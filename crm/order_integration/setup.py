import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def after_install():
    """Run after app installation - add custom fields to CRM Lead"""
    try:
        # Check if field already exists
        if not frappe.db.exists("Custom Field", "CRM Lead-order_status"):
            create_custom_fields({
                "CRM Lead": [
                    {
                        "fieldname": "order_status",
                        "fieldtype": "Data",
                        "label": "Order Status",
                        "insert_after": "status",
                        "in_list_view": 1,
                        "in_standard_filter": 0,
                        "search_index": 0,
                        "reqd": 0
                    }
                ]
            })
            frappe.db.commit()
        
        # Add order syncing settings to FCRM Settings
        if not frappe.db.exists("Custom Field", "FCRM Settings-order_integration_tab"):
            create_custom_fields({
                "FCRM Settings": [
                    {
                        "fieldname": "order_integration_tab",
                        "fieldtype": "Tab Break",
                        "label": "Order Integration",
                        "insert_after": "dropdown_items"
                    },
                    {
                        "fieldname": "enable_order_syncing",
                        "fieldtype": "Check",
                        "label": "Enable Order Syncing",
                        "insert_after": "order_integration_tab",
                        "default": 1
                    }
                ]
            })
            frappe.db.commit()
        
        # Setup the DocType Layout
        from order_integration.order_integration.doctype_layout import setup_crm_lead_layout
        setup_crm_lead_layout()
        
        # Setup the Order Source filter field
        from order_integration.order_integration.api.setup_order_source_field import setup_order_source_filter
        setup_order_source_filter()
        
    except Exception as e:
        frappe.log_error(f"Setup error: {str(e)}", "Order Integration Setup")


def setup_order_status_column():
    """Ensure order_status column is visible in list view and NOT as a filter"""
    try:
        # Get the custom field
        custom_field = frappe.get_doc("Custom Field", "CRM Lead-order_status")
        
        # Update settings
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
        
        # Setup the DocType Layout
        from order_integration.order_integration.doctype_layout import setup_crm_lead_layout
        setup_crm_lead_layout()
        
    except frappe.DoesNotExistError:
        pass
    except Exception as e:
        frappe.log_error(f"Setup column error: {str(e)}", "Order Integration Setup")