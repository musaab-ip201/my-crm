"""
Lead List Dynamic Columns API
Fetches external data (cart / ticket) for visible leads and returns
column definitions + per-lead row data so the frontend can inject
extra columns into the CRM Lead list view.
"""

import frappe
from frappe import _
import requests
import json
import re
from urllib.parse import urlparse

# ── Helpers ───────────────────────────────────────────────────────────────────


def _get_base_url(api_url: str) -> str:
    parsed = urlparse(api_url)
    return f"{parsed.scheme}://{parsed.netloc}"


def _fetch_with_auth(url, source, params=None):
    """Try multiple auth header formats; return parsed JSON on first 200 response."""
    access_token = None
    try:
        access_token = source.get_password("access_token")
    except Exception:
        pass
    if not access_token:
        access_token = source.access_token or ""

    api_key = source.api_key or ""

    header_formats = [
        {
            "crm-api-key": api_key,
            "crm-api-token": access_token,
            "Content-Type": "application/json",
        },
        {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        {
            "X-API-Token": access_token,
            "Content-Type": "application/json",
        },
        {
            "X-API-Key": api_key,
            "X-API-Token": access_token,
            "Content-Type": "application/json",
        },
    ]

    last_error = None
    for headers in header_formats:
        try:
            resp = requests.get(
                url, headers=headers, params=params, timeout=30, verify=True
            )
            if resp.status_code == 200:
                return resp.json()
            last_error = f"HTTP {resp.status_code}"
        except Exception as e:
            last_error = str(e)

    raise Exception(f"All auth formats failed for {url}. Last error: {last_error}")


def _extract_records(raw, nested_key):
    """Unwrap API response payloads cleanly into a standard flat list of dicts."""
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict):
        if nested_key and nested_key in raw and isinstance(raw[nested_key], list):
            return raw[nested_key]
        for key in ("data", "records", "items", "results"):
            if key in raw and isinstance(raw[key], list):
                return raw[key]
        return [raw]
    return []


def flatten_dict(data, parent_key="", sep="_"):
    """
    Recursively flattens nested dictionaries.
    Handles nested arrays of objects (like associated_products) cleanly
    by mapping the structural keys of the first item found.
    """
    items = {}
    if not isinstance(data, dict):
        return items

    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k

        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep))
        elif isinstance(v, list):
            # If it's an array containing objects, peek at the first item for column schema matching
            if v and isinstance(v[0], dict):
                items.update(flatten_dict(v[0], new_key, sep))
            # Safe fallbacks for simple array elements
            elif v and isinstance(v[0], (str, int, float)):
                items[new_key] = v[0]
            else:
                items[new_key] = ""
        else:
            items[new_key] = v
    return items


def normalize_phone(p):
    """Removes all non-numeric characters for reliable comparison."""
    return re.sub(r"\D", "", str(p)) if p else ""


# ── Public API ────────────────────────────────────────────────────────────────


@frappe.whitelist()
def get_available_data_types(source_name=None):
    """Return explicit unique data type filter settings configured inside system sources."""
    try:
        sources = frappe.get_all(
            "Order Sync Source", fields=["source_type", "source_name"]
        )
        all_types = [
            {"value": s.source_type, "label": s.source_name}
            for s in sources
            if s.source_type
        ]

        seen = set()
        unique_types = []
        for t in all_types:
            if t["value"] not in seen:
                seen.add(t["value"])
                unique_types.append(t)

        if not source_name:
            return unique_types

        source_type = (
            frappe.db.get_value("Order Sync Source", source_name, "source_type") or ""
        )
        if source_type in ("both", ""):
            return unique_types
        return [t for t in unique_types if t["value"] == source_type]
    except Exception:
        return []


@frappe.whitelist()
def get_dynamic_columns_data(source_name, data_type, lead_names=None):
    """
    Processes a source endpoint to dynamically discover active column mappings
    and returns localized matched data mapping rows back to target lead names.
    """
    try:
        if isinstance(lead_names, str):
            lead_names = json.loads(lead_names)
        if not lead_names:
            lead_names = []

        # ── 1. Verify Source configuration ────────────────────────────────────
        source = frappe.get_doc("Order Sync Source", source_name)
        if not source.api_url:
            return {"status": "error", "message": "Source has no API URL"}

        # ── 2. Query target CRM Lead matching identifiers ─────────────────────
        leads_info = {}
        if lead_names:
            rows = frappe.db.sql(
                """
                SELECT name, email, mobile_no
                FROM `tabCRM Lead`
                WHERE name IN %s
                """,
                [lead_names],
                as_dict=True,
            )
            for r in rows:
                leads_info[r.name] = {
                    "email": (r.email or "").strip().lower(),
                    "phone": (r.mobile_no or "").strip(),
                }

        # ── 3. Dispatch data sync requests ───────────────────────────────────
        endpoint = source.api_url
        fetch_params = {"page": 1, "limit": 1000}
        if data_type and data_type not in ("both", ""):
            fetch_params["type"] = data_type

        raw = _fetch_with_auth(endpoint, source, params=fetch_params)

        nested_key = None
        if isinstance(raw, dict):
            for key in ("data", "records", "items", "results"):
                if key in raw and isinstance(raw[key], list):
                    nested_key = key
                    break

        raw_records = _extract_records(raw, nested_key)

        # ── 4. Standardize structures and build clean dynamic column labels ──
        records = []
        dynamic_columns = []
        seen_fields = set()

        for rec in raw_records:
            flat_rec = flatten_dict(rec)
            records.append(flat_rec)

            for field in flat_rec.keys():
                if field not in seen_fields:
                    seen_fields.add(field)
                    dynamic_columns.append(
                        {"field": field, "label": field.replace("_", " ").title()}
                    )

        # ── 5. Index responses by contact endpoints for instant lookup ───────
        by_phone = {}
        by_email = {}

        email_fields = [
            "email",
            "customer_email",
            "contact_email",
            "user_email",
            "customer_api_email",
        ]
        phone_fields = [
            "phone",
            "customer_phone",
            "mobile",
            "mobile_no",
            "telephone",
            "customer_telephone",
        ]

        for rec in records:
            rec_email = ""
            rec_phone = ""

            for f in email_fields:
                if rec.get(f):
                    rec_email = str(rec.get(f)).strip().lower()
                    break

            if not rec_email:
                for k, v in rec.items():
                    if "email" in k.lower() and v and isinstance(v, str) and "@" in v:
                        rec_email = v.strip().lower()
                        break

            for f in phone_fields:
                if rec.get(f):
                    rec_phone = normalize_phone(rec.get(f))
                    break

            if not rec_phone:
                for k, v in rec.items():
                    lk = k.lower()
                    if ("phone" in lk or "mobile" in lk or "tel" in lk) and v:
                        rec_phone = normalize_phone(v)
                        break

            if rec_phone and rec_phone not in by_phone:
                by_phone[rec_phone] = rec
            if rec_email and rec_email not in by_email:
                by_email[rec_email] = rec

        # ── 6. Assemble output results map ───────────────────────────────────
        result_rows = {}

        for lead_id, info in leads_info.items():
            matched = None
            lead_phone = normalize_phone(info["phone"])
            lead_email = info["email"]

            if lead_phone and lead_phone in by_phone:
                matched = by_phone[lead_phone]
            elif lead_email and lead_email in by_email:
                matched = by_email[lead_email]

            if matched:
                result_rows[lead_id] = matched

        return {
            "status": "success",
            "data_type": data_type,
            "source_name": source_name,
            "columns": dynamic_columns,
            "rows": result_rows,
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Lead List Dynamic Columns API Error")
        return {"status": "error", "message": str(e)}
