import frappe

def customize_crm_lead_status(doc, method=None):
    """Add order status values to CRM Lead status field"""
    try:
        # Get the CRM Lead DocType
        doctype = frappe.get_doc("DocType", "CRM Lead")
        
        # Find the status field
        status_field = None
        for field in doctype.fields:
            if field.fieldname == "status":
                status_field = field
                break
        
        if not status_field:
            return
        
        # Get existing options
        existing_options = status_field.options or ""
        options_list = [opt.strip() for opt in existing_options.split("\n") if opt.strip()]
        
        # Add new status values if not already present
        new_statuses = ["Placed", "Added to Cart", "Rejected"]
        for status in new_statuses:
            if status not in options_list:
                options_list.append(status)
        
        # Update the field options
        status_field.options = "\n".join(options_list)
        
        # Save the DocType without triggering validation
        doctype.save(ignore_permissions=True)
        frappe.db.commit()
        
        print(f"✅ CRM Lead status field updated with new values: {new_statuses}")
        
    except Exception as e:
        print(f"❌ Error updating CRM Lead status: {str(e)}")
        frappe.log_error(f"Error updating CRM Lead status: {str(e)}", "Order Integration Error")
