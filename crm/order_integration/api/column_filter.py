"""
Column filtering API for Order Integration.

Provides two things:
1. get_columns_for_source  — returns the field names that belong to a
   specific Order Sync Source (used by the frontend to filter the
   "Add Column" dropdown).
2. get_all_source_field_map — returns a mapping of every api_col_* field
   to its source name (used by the frontend to hide irrelevant columns
   when an order_source filter is active).
"""

import frappe


@frappe.whitelist()
def get_columns_for_source(source_name):
    """
    Return the list of custom field names that were created for a specific
    Order Sync Source.

    These fields are identified by the description metadata stored when
    the field was created:  description = "api_source:<source_name>"
    """
    try:
        if not source_name:
            return {"status": "success", "fields": []}

        fields = frappe.get_all(
            "Custom Field",
            filters={
                "dt": "CRM Lead",
                "fieldname": ["like", "api_col_%"],
                "description": ["like", f"api_source:{source_name}%"],
            },
            fields=["fieldname", "label", "fieldtype"],
            order_by="label asc",
        )

        return {"status": "success", "fields": fields}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Column Filter Error")
        return {"status": "error", "message": str(e), "fields": []}


@frappe.whitelist()
def get_all_source_field_map():
    """
    Return a dict mapping every api_col_* fieldname → source_name.

    Example:
    {
        "api_col_mystore_customer_id": "MyStore",
        "api_col_mystore_quantity":    "MyStore",
        "api_col_shopx_order_id":      "ShopX",
    }

    The frontend uses this to:
    - Show ALL api_col fields when no order_source filter is active.
    - Show ONLY the matching source's fields when order_source is filtered.
    """
    try:
        fields = frappe.get_all(
            "Custom Field",
            filters={
                "dt": "CRM Lead",
                "fieldname": ["like", "api_col_%"],
            },
            fields=["fieldname", "description"],
        )

        field_map = {}
        for f in fields:
            desc = f.get("description") or ""
            if "api_source:" in desc:
                source = desc.split("api_source:")[1].strip()
                field_map[f["fieldname"]] = source

        return {"status": "success", "field_map": field_map}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Column Filter Error")
        return {"status": "error", "message": str(e), "field_map": {}}
