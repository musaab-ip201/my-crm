"""
API endpoints for CRM Lead customization
"""

import frappe
from frappe import _


@frappe.whitelist()
def get_crm_leads_with_order_status(filters=None, order_by=None, limit_page_length=20, limit_start=0):
    """
    Get CRM Leads with order_status field included
    This endpoint is called by the CRM frontend to fetch leads with order status
    """
    try:
        # Parse filters if provided as JSON string
        if isinstance(filters, str):
            import json
            filters = json.loads(filters)
        
        # Build the query
        query = frappe.qb.from_("tabCRM Lead").select(
            "name",
            "lead_name",
            "organization",
            "status",
            "order_status",
            "email",
            "mobile_no",
            "assigned_to",
            "modified",
            "creation"
        )
        
        # Apply filters
        if filters:
            for field, value in filters.items():
                if field == "converted":
                    query = query.where(frappe.qb.Field(field) == value)
                elif isinstance(value, list):
                    query = query.where(frappe.qb.Field(field).isin(value))
                else:
                    query = query.where(frappe.qb.Field(field) == value)
        
        # Apply ordering
        if order_by:
            query = query.orderby(order_by)
        else:
            query = query.orderby("modified", order="desc")
        
        # Apply pagination
        query = query.limit(limit_page_length).offset(limit_start)
        
        # Execute query
        results = query.run(as_dict=True)
        
        return {
            "status": "success",
            "data": results,
            "count": len(results)
        }
        
    except Exception as e:
        frappe.log_error(f"Error fetching CRM leads: {str(e)}", "CRM Lead API")
        return {
            "status": "error",
            "message": str(e),
            "data": []
        }


@frappe.whitelist()
def get_lead_order_status(lead_name):
    """
    Get order status for a specific lead
    """
    try:
        order_status = frappe.db.get_value("CRM Lead", lead_name, "order_status")
        return {
            "status": "success",
            "order_status": order_status
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


print("[ORDER_INTEGRATION] ✅ crm_lead_api.py loaded")
