"""
DocType Layout customization for CRM Lead list view
This module ensures the order_status field is properly configured for list view display.
"""

import frappe


def setup_crm_lead_layout():
    """
    Ensure order_status field is properly configured for list view display
    """
    try:
        # Get the custom field
        custom_field = frappe.get_doc("Custom Field", "CRM Lead-order_status")
        
        # Ensure it's configured for list view
        updated = False
        
        if not custom_field.in_list_view:
            custom_field.in_list_view = 1
            updated = True
        
        if custom_field.in_standard_filter:
            custom_field.in_standard_filter = 0
            updated = True
        
        if custom_field.search_index:
            custom_field.search_index = 0
            updated = True
        
        if updated:
            custom_field.save(ignore_permissions=True)
            frappe.db.commit()
        
        # Clear cache to ensure changes are reflected
        frappe.clear_cache()
        
    except frappe.DoesNotExistError:
        pass
    except Exception as e:
        frappe.log_error(f"Layout setup error: {str(e)}", "Order Integration Setup")
