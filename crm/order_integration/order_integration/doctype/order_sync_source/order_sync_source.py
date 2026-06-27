import frappe
from frappe import _
from frappe.model.document import Document
import requests
import json
from urllib.parse import urlparse
import time


class OrderSyncSource(Document):
    """Order Sync Source DocType"""

    def validate(self):
        """Validate Order Sync Source on save"""
        self.validate_api_url()
        # [START 11/5/26 siddhali]
        self._auto_set_source_type()
        # [END 11/5/26 siddhali]

    # [START 11/5/26 siddhali]
    def _auto_set_source_type(self):
        """
        Auto-detect source_type from source_name only if not already set.
        """
        if self.source_type:
            return  # already set by user — respect it

        # Only auto-set if source_name is provided and source_type is blank
        if self.source_name:
            name_lower = self.source_name.lower()
            if "seller" in name_lower or "ticket" in name_lower:
                self.source_type = "ticket_data"
            elif "customer" in name_lower or "cart" in name_lower or "buyer" in name_lower:
                self.source_type = "cart_data"
            else:
                import re
                slug = re.sub(r'[^a-zA-Z0-9]+', '_', self.source_name).strip('_').lower()
                self.source_type = slug
    # [END 11/5/26 siddhali]

    def validate_api_url(self):
        """Validate that API URL is a valid URL"""
        api_url = self.api_url or ""
        if not api_url:
            frappe.throw(_("API URL is required"))

        try:
            result = urlparse(api_url)
            if not all([result.scheme, result.netloc]):
                frappe.throw(_("API URL must be a valid URL (e.g., https://api.example.com/orders)"))
        except Exception:
            frappe.throw(_("API URL is invalid"))


@frappe.whitelist()
def save_order_source(doc, is_edit=False):
    """Save Order Sync Source document"""
    try:
        # Handle if doc is passed as JSON string
        if isinstance(doc, str):
            doc = json.loads(doc)

        if is_edit:
            source_name = doc.get("name")
            order_doc = frappe.get_doc("Order Sync Source", source_name)
            order_doc.source_name = doc.get("source_name")
            order_doc.api_key = doc.get("api_key")
            order_doc.sync_frequency = doc.get("sync_frequency")
            order_doc.api_url = doc.get("api_url")
            if doc.get("source_type"):
                order_doc.source_type = doc.get("source_type")

            # Only update token if provided
            if doc.get("access_token"):
                order_doc.access_token = doc.get("access_token")

            order_doc.save(ignore_permissions=True)
            frappe.db.commit()

            return {"status": "success", "message": "Source updated successfully", "name": order_doc.name}
        else:
            order_doc = frappe.get_doc({
                "doctype": "Order Sync Source",
                "source_name": doc.get("source_name"),
                "api_key": doc.get("api_key"),
                "sync_frequency": doc.get("sync_frequency"),
                "source_type": doc.get("source_type") or "",
                "api_url": doc.get("api_url"),
                "access_token": doc.get("access_token")
            })

            order_doc.insert(ignore_permissions=True)
            frappe.db.commit()

            return {"status": "success", "message": "Source created successfully", "name": order_doc.name}
    except Exception as e:
        frappe.log_error(title="Order Sync Save Error", message=frappe.get_traceback())
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def sync_orders_now(source_name):
    """Sync orders from API and create leads"""
    import traceback as tb

    def _log(msg):
        frappe.log_error(title="Order Sync Debug", message=msg)

    try:
        _log(f"[1] Starting sync for source: {source_name}")
        source = frappe.get_doc("Order Sync Source", source_name)
        _log(f"[2] Source loaded: name={source.name} url={source.api_url} type={source.source_type}")

        if not source.api_url:
            _log("[ERR] API URL is not configured")
            return {"status": "error", "message": "API URL is not configured", "orders": [], "leads_created": 0}

        orders = _fetch_orders_from_api(source)
        _log(f"[3] Fetched {len(orders) if orders else 0} orders from API")

        if not orders:
            _log("[ERR] No orders fetched — check API credentials and endpoint")
            return {"status": "error", "message": "No orders fetched from API - check API credentials and endpoint", "orders": [], "leads_created": 0}

        leads_created = []
        leads_skipped = []
        leads_errors = []

        for idx, order in enumerate(orders, 1):
            try:
                result = _create_lead_from_order(order, source)
                _log(f"[4.{idx}] Order result: {result.get('status')} — {result.get('reason','')}")

                if result["status"] == "created":
                    leads_created.append({
                        "lead_name": result["lead_id"],
                        "customer_name": result.get("customer_name"),
                        "email": result.get("email"),
                        "phone": result.get("phone")
                    })
                elif result["status"] == "skipped":
                    leads_skipped.append({
                        "reason": result["reason"],
                        "order_data": order
                    })
                else:
                    leads_errors.append({
                        "error": result.get("reason", "Unknown error"),
                        "order_data": order
                    })
            except Exception as e:
                error_msg = str(e)
                leads_errors.append({
                    "error": error_msg,
                    "order_data": order
                })
                frappe.log_error(title="Order Sync Error", message=f"Error creating lead from order: {error_msg}\n{frappe.get_traceback()}")

        frappe.db.set_value("Order Sync Source", source_name, "last_synced_at", frappe.utils.now())
        frappe.db.commit()

        return {
            "status": "success",
            "message": f"Sync completed: {len(leads_created)} leads created, {len(leads_skipped)} skipped, {len(leads_errors)} errors",
            "orders_total": len(orders),
            "leads_created": leads_created,
            "leads_skipped": leads_skipped,
            "leads_errors": leads_errors
        }
    except Exception as e:
        error_msg = f"Sync failed: {str(e)}"
        frappe.log_error(title="Order Sync Error", message=frappe.get_traceback())
        return {"status": "error", "message": error_msg, "orders": [], "leads_created": 0}


def _fetch_orders_from_api(source):
    """Fetch orders from external API with multiple authentication format support"""
    max_retries = 3
    retry_delay = 2

    # Get the access token - IMPORTANT: Password fields need get_password()
    access_token = None

    # Try Method 1: Use get_password() which handles decryption
    try:
        access_token = source.get_password("access_token")
    except Exception:
        pass

    # Try Method 2: Direct attribute access
    if not access_token:
        try:
            access_token = source.access_token
        except Exception:
            pass

    # Try Method 3: Query database directly
    if not access_token:
        try:
            db_token = frappe.db.get_value("Order Sync Source", source.name, "access_token")
            if db_token:
                access_token = db_token
        except Exception:
            pass

    if not access_token:
        frappe.log_error(title="Order Sync Error", message="No access token in Order Sync Source")
        return []

    # Define all header format combinations to try
    header_formats = [
        {
            "name": "Custom Headers (crm-api-key + crm-api-token)",
            "headers": {
                "crm-api-key": source.api_key,
                "crm-api-token": access_token,
                "Content-Type": "application/json"
            }
        },
        {
            "name": "Bearer Token (Authorization header)",
            "headers": {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        },
        {
            "name": "X-API-Token Header",
            "headers": {
                "X-API-Token": access_token,
                "Content-Type": "application/json"
            }
        },
        {
            "name": "X-API-Key Header",
            "headers": {
                "X-API-Key": source.api_key,
                "X-API-Token": access_token,
                "Content-Type": "application/json"
            }
        },
        {
            "name": "API-Key Header",
            "headers": {
                "API-Key": source.api_key,
                "API-Token": access_token,
                "Content-Type": "application/json"
            }
        }
    ]

    for attempt in range(max_retries):
        for format_config in header_formats:
            try:
                response = requests.get(
                    source.api_url,
                    headers=format_config['headers'],
                    timeout=15,
                    verify=True
                )

                # If successful, process and return data
                if response.status_code == 200:
                    data = response.json()
                    frappe.log_error(title="Order Sync Debug", message=f"API success with format: {format_config['name']} — got {type(data).__name__} with {len(data) if isinstance(data, (list,dict)) else '?'} items")

                    # Handle different response formats
                    if isinstance(data, dict):
                        if "data" in data:
                            data = data["data"]
                        elif "orders" in data:
                            data = data["orders"]
                        elif "results" in data:
                            data = data["results"]
                        elif "records" in data:
                            data = data["records"]
                        elif "items" in data:
                            data = data["items"]
                        else:
                            data = [data]

                    if not isinstance(data, list):
                        data = [data]

                    return data

                # If 401, try next format
                if response.status_code == 401:
                    frappe.log_error(title="Order Sync Debug", message=f"401 with format: {format_config['name']}")
                    continue

                # Other errors
                if response.status_code != 200:
                    frappe.log_error(title="Order Sync Debug", message=f"HTTP {response.status_code} with format: {format_config['name']} — body: {response.text[:200]}")
                    continue

            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                frappe.log_error(title="Order Sync Error", message=f"API network error for URL {source.api_url}: {str(e)}")
                # Network error — no point trying other header formats, go to next retry
                break
            except Exception:
                continue

        # If all formats failed, wait before retry
        if attempt < max_retries - 1:
            time.sleep(retry_delay)
            retry_delay *= 2

    frappe.log_error(title="Order Sync Error", message=f"All authentication formats failed for API: {source.api_url}")
    return []


def _create_lead_from_order(order_data, source):
    """Create a CRM Lead from order data"""
    try:
        # Extract customer info from nested structure
        customer_info = order_data.get("customer", {})

        # Get customer name - try multiple fields
        customer_name = (
            customer_info.get("name") or
            order_data.get("customer_name") or
            order_data.get("name") or
            f"Customer {customer_info.get('id', 'Unknown')}"
        )

        # Get email
        email = (customer_info.get("email") or order_data.get("email") or "").strip()

        # Get phone
        phone = (customer_info.get("telephone") or customer_info.get("phone") or order_data.get("phone") or "").strip()

        # Get order status
        order_status = order_data.get("order_status") or ""

        # Validate: at least email or phone required
        if not email and not phone:
            reason = "No email or phone found"
            return {"status": "skipped", "reason": reason}

        # Normalize phone
        if phone:
            phone = ''.join(filter(str.isdigit, phone))

        # Check for duplicates - PER SOURCE (skip if already created in THIS source before)
        # Allow same customer from different sources

        # Check email in this source only
        if email:
            existing_lead = frappe.db.get_value("CRM Lead", {"email": email, "order_source": source.name})
            if existing_lead:
                reason = f"Email already exists in this source: {email}"
                return {"status": "skipped", "reason": reason}

        # Check phone in this source only
        if phone:
            existing_lead = frappe.db.get_value("CRM Lead", {"mobile_no": phone, "order_source": source.name})
            if existing_lead:
                reason = f"Phone already exists in this source: {phone}"
                return {"status": "skipped", "reason": reason}

        # Validate status exists
        status = order_status if order_status else "New"
        if not frappe.db.exists("CRM Lead Status", status):
            status = "New"

        # Split customer name into first and last name
        name_parts = customer_name.split(' ', 1)
        first_name = name_parts[0] if name_parts else "Customer"
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        # Create lead using raw SQL
        lead_id = frappe.generate_hash(length=12)
        now = frappe.utils.now()

        # In background jobs frappe.session.user is "Guest" — fall back to Administrator
        session_user = frappe.session.user
        if not session_user or session_user in ("Guest", ""):
            session_user = "Administrator"

        # Insert into CRM Lead table with all required fields
        # lead_owner is set to the session user so dashboard counts include this lead
        sql_query = """
            INSERT INTO `tabCRM Lead`
            (name, first_name, last_name, lead_name, email, mobile_no, status, lead_owner, creation, modified, owner, modified_by, docstatus)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        sql_values = (
            lead_id,
            first_name,
            last_name,
            customer_name,
            email if email else None,
            phone if phone else None,
            status,
            session_user,
            now,
            now,
            session_user,
            session_user,
            0
        )

        try:
            frappe.db.sql(sql_query, sql_values)
        except Exception as sql_error:
            raise sql_error

        frappe.db.commit()

        # Update order_source field to link to the Order Sync Source
        try:
            frappe.db.set_value("CRM Lead", lead_id, "order_source", source.name)
            frappe.db.commit()
        except Exception as e:
            frappe.log_error(title="Order Sync Warning", message=f"Failed to set order_source: {str(e)}")

        # [START 11/5/26 siddhali]
        # Clear ALL existing Frappe assignments (stacked by on_lead_created hook)
        # then do a single clean assignment based on source type.
        try:
            from frappe.desk.form.assign_to import clear as assign_clear
            assign_clear("CRM Lead", lead_id, ignore_permissions=True)
        except Exception:
            pass

        # Route lead to the correct support team based on the source's department tag.
        # cart_data  → Customer Support team
        # ticket_data → Seller Support team
        assigned = False
        try:
            from order_integration.order_integration.api.customer_assignment import (
                assign_by_source_department,
            )
            assigned = assign_by_source_department(lead_id, source.name)
        except Exception as e:
            frappe.log_error(title="Order Sync Warning", message=f"Support assignment failed (non-fatal): {str(e)}\n{frappe.get_traceback()}")
            assigned = False
        # [END 11/5/26 siddhali]

        # If custom assignment failed, fallback to lead_routing
        if not assigned:
            try:
                lead_doc = frappe.get_doc("CRM Lead", lead_id)
                lead_doc.flags.skip_auto_assignment = True
                from lead_routing.api.lead_transfer import on_lead_created
                on_lead_created(lead_doc, method="after_insert")
            except ImportError:
                pass  # lead_routing not installed
            except Exception as e:
                frappe.log_error(title="Order Sync Warning", message=f"Lead routing assignment failed (non-fatal): {str(e)}")

        return {
            "status": "created",
            "lead_id": lead_id,
            "customer_name": customer_name,
            "email": email,
            "phone": phone
        }

    except Exception as e:
        error_msg = f"Error creating lead: {str(e)}"
        frappe.log_error(title="Order Sync Error", message=f"{error_msg}\n{frappe.get_traceback()}")
        return {"status": "error", "reason": error_msg}


@frappe.whitelist()
def get_order_sources():
    """Get all Order Sync Source documents"""
    try:
        return frappe.get_all(
            "Order Sync Source",
            fields=["name", "source_name", "api_key", "api_url", "sync_frequency", "last_synced_at"],
            order_by="creation desc"
        )
    except Exception as e:
        frappe.log_error(title="Order Sync Get Sources Error", message=frappe.get_traceback())
        return []


@frappe.whitelist()
def test_api_connection(api_url, access_token, api_key="ipshopy"):
    """Test API connection with multiple authentication formats"""
    try:
        # Define all header format combinations to try
        header_formats = [
            {
                "name": "Custom Headers (crm-api-key + crm-api-token)",
                "headers": {
                    "crm-api-key": api_key,
                    "crm-api-token": access_token,
                    "Content-Type": "application/json"
                }
            },
            {
                "name": "Bearer Token (Authorization header)",
                "headers": {
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                }
            },
            {
                "name": "X-API-Token Header",
                "headers": {
                    "X-API-Token": access_token,
                    "Content-Type": "application/json"
                }
            },
            {
                "name": "X-API-Key Header",
                "headers": {
                    "X-API-Key": api_key,
                    "X-API-Token": access_token,
                    "Content-Type": "application/json"
                }
            },
            {
                "name": "API-Key Header",
                "headers": {
                    "API-Key": api_key,
                    "API-Token": access_token,
                    "Content-Type": "application/json"
                }
            }
        ]

        for format_config in header_formats:
            try:
                response = requests.get(api_url, headers=format_config['headers'], timeout=10, verify=True)

                if response.status_code == 200:
                    data = response.json()

                    # Handle different response formats
                    if isinstance(data, dict):
                        if "data" in data:
                            data = data["data"]
                        elif "orders" in data:
                            data = data["orders"]
                        elif "results" in data:
                            data = data["results"]
                        elif "records" in data:
                            data = data["records"]
                        elif "items" in data:
                            data = data["items"]

                    if not isinstance(data, list):
                        data = [data]

                    return {
                        "status": "success",
                        "message": f"API connection successful! Found {len(data)} records (using: {format_config['name']})",
                        "sample_record": data[0] if data else None
                    }
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                return {"status": "error", "message": f"Network Error: Unable to connect to API ({str(e)})"}
            except Exception:
                continue

        # If all formats failed
        return {"status": "error", "message": "Authentication failed: No authentication format worked"}

    except Exception as e:
        return {"status": "error", "message": f"Connection failed: {str(e)}"}


@frappe.whitelist()
def trigger_manual_sync(source_name):
    """Trigger manual sync for a single source"""
    return sync_orders_now(source_name)


@frappe.whitelist()
def trigger_sync_all():
    """Trigger sync for all sources"""
    try:
        sources = frappe.get_all("Order Sync Source", fields=["name"])
        synced_count = 0

        for source in sources:
            try:
                sync_orders_now(source.name)
                synced_count += 1
            except Exception as e:
                frappe.log_error(title="Order Sync Error", message=f"Error syncing source {source.name}: {str(e)}")

        return {
            "status": "success",
            "message": f"Synced {synced_count} sources",
            "synced_count": synced_count
        }
    except Exception as e:
        frappe.log_error(title="Order Sync All Error", message=frappe.get_traceback())
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def delete_order_source(source_name):
    """Delete an Order Sync Source"""
    try:
        frappe.delete_doc("Order Sync Source", source_name)
        frappe.db.commit()
        return {"status": "success", "message": "Source deleted"}
    except Exception as e:
        frappe.log_error(title="Order Sync Delete Error", message=frappe.get_traceback())
        return {"status": "error", "message": str(e)}


# [START 11/5/26 siddhali]
@frappe.whitelist()
def backfill_source_types():
    """
    One-time backfill: auto-detect and set source_type for all existing
    Order Sync Source records that have a blank source_type.

    Run once in bench console:
      from order_integration.order_integration.doctype.order_sync_source.order_sync_source import backfill_source_types
      backfill_source_types()
    """
    sources = frappe.get_all(
        "Order Sync Source",
        filters={"source_type": ["in", ["", None]]},
        fields=["name", "source_name"],
    )

    updated = []
    for s in sources:
        import re
        slug = re.sub(r'[^a-zA-Z0-9]+', '_', s.source_name or "dynamic").strip('_').lower()
        frappe.db.set_value("Order Sync Source", s.name, "source_type", slug)
        updated.append({"name": s.name, "source_type": slug})

    frappe.db.commit()
    return {"status": "success", "updated": updated}
# [END 11/5/26 siddhali]


# [START 11/5/26 siddhali]
def run_scheduled_sync_by_frequency():
    """
    Called by the Frappe scheduler (hooks.py cron entries).
    Runs sync for every Order Sync Source whose sync_frequency
    matches the current cron interval.

    Cron fires at: */5, */10, 0 * (hourly), 0 0 (daily)
    Each call checks which sources are due and syncs only those.
    """
    import datetime

    now = frappe.utils.now_datetime()
    minute = now.minute
    hour = now.hour

    # Map sync_frequency label → "is this cron tick the right one?"
    def is_due(freq):
        if freq == "Every 5 Minutes":
            return True                          # fires on every */5 tick
        if freq == "Every 10 Minutes":
            return minute % 10 == 0             # fires on */10 ticks
        if freq == "Hourly":
            return minute == 0                  # fires once per hour
        if freq == "Daily":
            return minute == 0 and hour == 0    # fires at midnight only
        return False

    sources = frappe.get_all(
        "Order Sync Source",
        fields=["name", "sync_frequency"],
    )

    for source in sources:
        if not is_due(source.sync_frequency):
            continue
        try:
            sync_orders_now(source.name)
        except Exception:
            frappe.log_error(
                title=f"Scheduled Sync Failed: {source.name}",
                message=frappe.get_traceback(),
            )
# [END 11/5/26 siddhali]
