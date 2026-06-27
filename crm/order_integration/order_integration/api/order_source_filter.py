"""
Custom filter for Order Source in CRM Lead list view
Shows source_name instead of ID
"""

import frappe


@frappe.whitelist()
def get_order_source_filter_options():
    """
    Get order source options for filter dropdown
    Returns list with label (source_name) and value (name)
    """
    try:
        sources = frappe.get_all(
            "Order Sync Source",
            fields=["name", "source_name"],
            order_by="source_name asc",
        )

        # Format for Frappe filter dropdown
        options = []
        for source in sources:
            options.append(
                {"label": source.source_name or source.name, "value": source.name}
            )

        return options
    except Exception as e:
        frappe.log_error(
            f"Error getting order source options: {str(e)}", "Order Integration"
        )
        return []


print("[ORDER_INTEGRATION] ✅ order_source_filter.py loaded")
