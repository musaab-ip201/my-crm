"""
Lead Source Data API
Fetches source-specific data for a CRM Lead from its linked Order Sync Source.
"""

import re
import json
import frappe
from frappe import _
import requests
from urllib.parse import urlparse


def _normalize_phone(p):
    """Strip all non-digit characters for comparison."""
    return re.sub(r"\D", "", str(p)) if p else ""


def _fetch_with_auth(url: str, source, params: dict = None) -> dict:
    """Try multiple auth header formats; return parsed JSON on first 200."""
    access_token = None
    try:
        access_token = source.get_password("access_token")
    except Exception:
        pass
    if not access_token:
        access_token = source.access_token or ""

    api_key = source.api_key or ""

    header_formats = [
        {"crm-api-key": api_key, "crm-api-token": access_token, "Content-Type": "application/json"},
        {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
        {"X-API-Token": access_token, "Content-Type": "application/json"},
        {"X-API-Key": api_key, "X-API-Token": access_token, "Content-Type": "application/json"},
    ]

    last_error = None
    for headers in header_formats:
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=30, verify=True)
            if resp.status_code == 200:
                return resp.json()
            last_error = f"HTTP {resp.status_code}"
        except Exception as e:
            last_error = str(e)

    raise Exception(f"All auth formats failed for {url}. Last error: {last_error}")


def _extract_records(raw) -> list:
    """Unwrap API response into a flat list of records."""
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict):
        for key in ("data", "records", "items", "results"):
            if key in raw and isinstance(raw[key], list):
                return raw[key]
        return [raw]
    return []


def _flatten(rec: dict, parent_key: str = "", sep: str = "_") -> dict:
    """Recursively flatten a nested dict."""
    items = {}
    for k, v in rec.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(_flatten(v, new_key, sep))
        elif isinstance(v, list):
            # Keep first scalar element or serialize
            if v and isinstance(v[0], (str, int, float, bool)):
                items[new_key] = v[0]
            else:
                items[new_key] = json.dumps(v)
        else:
            items[new_key] = v
    return items


@frappe.whitelist()
def get_data_types(lead_name: str = None):
    """
    Return available data type options for the panel dropdown.
    Scoped to the lead's linked Order Sync Source when lead_name is given.
    """
    try:
        if lead_name:
            order_source = frappe.db.get_value("CRM Lead", lead_name, "order_source")
            if order_source:
                source = frappe.db.get_value(
                    "Order Sync Source",
                    order_source,
                    ["source_type", "source_name"],
                    as_dict=True,
                )
                if source:
                    source_type = source.source_type or ""
                    if source_type == "both":
                        return [
                            {"value": "cart_data", "label": "Cart Data"},
                            {"value": "ticket_data", "label": "Ticket Data"},
                        ]
                    elif source_type:
                        # Return the specific type with the source's display name
                        label = source.source_name or source_type.replace("_", " ").title()
                        return [{"value": source_type, "label": label}]

        # Fallback: return all unique types across all sources
        sources = frappe.get_all("Order Sync Source", fields=["source_type", "source_name"])
        seen = set()
        result = []
        for s in sources:
            if s.source_type and s.source_type not in seen:
                seen.add(s.source_type)
                result.append({"value": s.source_type, "label": s.source_name or s.source_type})
        return result
    except Exception:
        return [
            {"value": "cart_data", "label": "Cart Data"},
            {"value": "ticket_data", "label": "Ticket Data"},
        ]


@frappe.whitelist()
def get_lead_source_data(lead_name: str, data_type: str = None, page: int = 1, page_size: int = 20):
    """
    Fetch source data for a CRM Lead from its linked Order Sync Source.
    Matches records by normalised phone or email.
    """
    try:
        page = int(page)
        page_size = int(page_size)

        # ── 1. Load lead ───────────────────────────────────────────────────────
        lead = frappe.db.get_value(
            "CRM Lead",
            lead_name,
            ["order_source", "mobile_no", "email", "lead_name"],
            as_dict=True,
        )
        if not lead:
            return {"status": "error", "message": "Lead not found"}

        if not lead.order_source:
            return {
                "status": "error",
                "message": "This lead has no Order Source linked.",
            }

        # ── 2. Load source ─────────────────────────────────────────────────────
        source = frappe.get_doc("Order Sync Source", lead.order_source)
        if not source.api_url:
            return {"status": "error", "message": "Order Source has no API URL configured"}

        # ── 3. Fetch all records (large page to cover all leads) ───────────────
        params = {"page": 1, "limit": 1000}
        if data_type and data_type not in ("both", ""):
            params["type"] = data_type

        raw = _fetch_with_auth(source.api_url, source, params)
        records = _extract_records(raw)

        # ── 4. Match by phone or email ─────────────────────────────────────────
        lead_phone = _normalize_phone(lead.mobile_no)
        lead_email = (lead.email or "").strip().lower()

        def matches(rec):
            # Check all keys that might contain phone or email
            flat = _flatten(rec)
            for k, v in flat.items():
                lk = k.lower()
                if v is None:
                    continue
                sv = str(v).strip()
                if not sv:
                    continue
                # Phone match
                if lead_phone and ("phone" in lk or "mobile" in lk or "tel" in lk):
                    if _normalize_phone(sv) == lead_phone:
                        return True
                # Email match
                if lead_email and "email" in lk:
                    if sv.lower() == lead_email:
                        return True
            return False

        matched = [r for r in records if matches(r)]

        if not matched:
            return {
                "status": "success",
                "records": [],
                "columns": [],
                "total_records": 0,
                "message": "No records found matching this lead's phone or email.",
            }

        # ── 5. Flatten all matched records ─────────────────────────────────────
        flat_records = [_flatten(r) for r in matched]

        # ── 6. Build column list from all matched records (union of keys) ──────
        seen_cols = set()
        columns = []
        for rec in flat_records:
            for k in rec.keys():
                if k not in seen_cols:
                    seen_cols.add(k)
                    columns.append(k)

        # ── 7. Paginate ────────────────────────────────────────────────────────
        total = len(flat_records)
        start = (page - 1) * page_size
        paginated = flat_records[start: start + page_size]

        return {
            "status": "success",
            "data_type": data_type or source.source_type,
            "label": source.source_name,
            "records": paginated,
            "columns": columns,
            "total_records": total,
            "page": page,
            "page_size": page_size,
            "lead_name": lead_name,
            "customer_name": lead.lead_name,
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Lead Source Data API Error")
        return {"status": "error", "message": str(e)}
