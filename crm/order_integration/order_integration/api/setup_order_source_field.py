"""
Setup Order Source field as a filter in CRM Lead
"""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def setup_order_source_filter():
    """
    Create order_source custom field in CRM Lead for filtering
    This field will appear as a filter dropdown in the Lead list view
    Shows source_name instead of ID
    """
    print("\n" + "="*80)
    print("[ORDER_INTEGRATION] Setting up Order Source filter field...")
    print("="*80 + "\n")
    
    try:
        # Check if field already exists
        if frappe.db.exists("Custom Field", "CRM Lead-order_source"):
            print("[ORDER_INTEGRATION] ✅ Order Source field already exists")
            # Update it to ensure correct settings
            field = frappe.get_doc("Custom Field", "CRM Lead-order_source")
            field.in_standard_filter = 1
            field.save(ignore_permissions=True)
            frappe.db.commit()
            print("[ORDER_INTEGRATION] ✅ Order Source field updated")
            return
        
        print("[ORDER_INTEGRATION] 📝 Creating Order Source custom field...")
        
        create_custom_fields({
            "CRM Lead": [
                {
                    "fieldname": "order_source",
                    "fieldtype": "Link",
                    "label": "Order Source",
                    "options": "Order Sync Source",
                    "insert_after": "status",
                    "in_list_view": 0,
                    "in_standard_filter": 1,  # Show as filter
                    "search_index": 0,
                    "reqd": 0
                }
            ]
        })
        
        frappe.db.commit()
        print("[ORDER_INTEGRATION] ✅ Order Source field created successfully")
        print("[ORDER_INTEGRATION] ✅ Field will appear as filter in Lead list view")
        print("[ORDER_INTEGRATION] ✅ Filter will show source_name (not ID)")
        
    except Exception as e:
        print(f"[ORDER_INTEGRATION] ❌ Error creating field: {str(e)}")
        frappe.log_error(f"Setup error: {str(e)}", "Order Integration Setup")


print("[ORDER_INTEGRATION] ✅ setup_order_source_field.py loaded")
