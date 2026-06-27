import frappe
import json
from crm.api.doc import get_data as original_get_data
from order_integration.order_integration.api.lead_list_dynamic_columns_api import (
    get_dynamic_columns_data,
)

@frappe.whitelist()
def get_data(
    doctype: str,
    filters: dict,
    order_by: str,
    page_length=20,
    page_length_count=20,
    column_field=None,
    title_field=None,
    columns=None,
    rows=None,
    kanban_columns=None,
    kanban_fields=None,
    view=None,
    default_filters=None,
):
    """
    Override the standard CRM get_data API to dynamically inject
    Order Source columns directly into the API response.
    """
    if isinstance(filters, str):
        filters = json.loads(filters)

    # Sanitize default_filters — strip any fields that don't exist on the
    # doctype table. A stale CRM View Settings record can contain fields like
    # 'date_added' that were never actual columns, causing MySQL error 1054.
    if default_filters and doctype:
        try:
            parsed = (
                frappe.parse_json(default_filters)
                if isinstance(default_filters, str)
                else dict(default_filters)
            )
            meta = frappe.get_meta(doctype)
            valid_fieldnames = {f.fieldname for f in meta.fields}
            standard_fields = {
                "name", "owner", "creation", "modified", "modified_by",
                "docstatus", "_assign", "_liked_by", "_user_tags", "_comments",
            }
            cleaned = {
                k: v
                for k, v in parsed.items()
                if k in valid_fieldnames or k in standard_fields or k.startswith("_")
            }
            default_filters = json.dumps(cleaned)
        except Exception:
            pass

    # Call original method to get standard data
    res = original_get_data(
        doctype=doctype,
        filters=filters,
        order_by=order_by,
        page_length=page_length,
        page_length_count=page_length_count,
        column_field=column_field,
        title_field=title_field,
        columns=columns,
        rows=rows,
        kanban_columns=kanban_columns,
        kanban_fields=kanban_fields,
        view=view,
        default_filters=default_filters,
    )

    # Only inject for CRM Lead
    if doctype != "CRM Lead":
        return res

    if not isinstance(filters, dict):
        res["_dynamic_columns"] = []
        return res

    # Find order_source filter value
    source_name = None
    for k, v in filters.items():
        if k.lower() in ("order_source", "source", "order_source_filter"):
            if isinstance(v, str) and v:
                source_name = v
            elif isinstance(v, list) and len(v) > 0:
                source_name = v[-1]
            break

    # No order_source filter → tell frontend to show no dynamic columns
    if not source_name:
        res["_dynamic_columns"] = []
        return res

    # Verify the source exists
    if not frappe.db.exists("Order Sync Source", source_name):
        res["_dynamic_columns"] = []
        return res

    # Grab the precise dynamic source layout data
    source_type = frappe.db.get_value("Order Sync Source", source_name, "source_type") or "cart_data"

    try:
        leads = [row.get("name") for row in res.get("data", []) if row.get("name")]
        if not leads:
            res["_dynamic_columns"] = []
            return res

        # Call our updated dynamic column fetcher
        dynamic = get_dynamic_columns_data(source_name, source_type, leads)

        if dynamic and dynamic.get("status") == "success":
            new_cols = dynamic.get("columns", [])
            dynamic_rows = dynamic.get("rows", {})

            # Inject _dynamic_columns for the frontend fetch interceptor
            res["_dynamic_columns"] = new_cols

            # Also inject into columns/rows/fields for native CRM table rendering
            for col in new_cols:
                if "columns" in res:
                    if not any(c.get("key") == col["field"] for c in res["columns"]):
                        res["columns"].append({
                            "label": col["label"],
                            "type": "Data",
                            "key": col["field"],
                            "width": "12rem",
                        })

                if "rows" in res:
                    if col["field"] not in res["rows"]:
                        res["rows"].append(col["field"])

                if "fields" in res:
                    if not any(f.get("fieldname") == col["field"] for f in res["fields"]):
                        res["fields"].append({
                            "label": col["label"],
                            "fieldtype": "Data",
                            "fieldname": col["field"],
                            "options": "",
                        })

            # Inject external data fields into each row matching the Lead Name
            for row in res.get("data", []):
                lead_id = row.get("name")
                if lead_id and lead_id in dynamic_rows:
                    row.update(dynamic_rows[lead_id])
        else:
            res["_dynamic_columns"] = []

    except Exception as e:
        frappe.log_error(title="Dynamic Columns Override API Error", message=str(e))
        res["_dynamic_columns"] = []

    return res