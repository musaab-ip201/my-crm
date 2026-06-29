"""API endpoint to setup CRM Lead Status values"""
import frappe


@frappe.whitelist()
def setup_crm_lead_statuses():
    """Create CRM Lead Status values for order syncing - can be called via API"""
    
    statuses_to_create = [
        {
            "name": "Placed",
            "status_name": "Placed",
            "description": "Order has been placed"
        },
        {
            "name": "Added to Cart",
            "status_name": "Added to Cart",
            "description": "Customer added item to cart"
        },
        {
            "name": "Rejected",
            "status_name": "Rejected",
            "description": "Order was rejected"
        }
    ]
    
    print("\n" + "="*80)
    print("CREATING CRM LEAD STATUS VALUES")
    print("="*80 + "\n")
    
    created = []
    already_exist = []
    errors = []
    
    for status_data in statuses_to_create:
        try:
            # Check if status already exists
            if frappe.db.exists("CRM Lead Status", status_data["name"]):
                print(f"✅ Status '{status_data['name']}' already exists")
                already_exist.append(status_data["name"])
                continue
            
            # Create new status
            status_doc = frappe.get_doc({
                "doctype": "CRM Lead Status",
                "name": status_data["name"],
                "status_name": status_data["status_name"],
                "description": status_data.get("description", "")
            })
            status_doc.insert(ignore_permissions=True)
            frappe.db.commit()
            print(f"✅ Created status: {status_data['name']}")
            created.append(status_data["name"])
        except Exception as e:
            error_msg = f"Error creating status '{status_data['name']}': {str(e)}"
            print(f"⚠️ {error_msg}")
            frappe.log_error(error_msg, "Order Integration Setup")
            errors.append(error_msg)
    
    print("\n" + "="*80)
    print("SETUP COMPLETED")
    print("="*80 + "\n")
    
    return {
        "status": "success" if not errors else "partial",
        "message": f"Created {len(created)} statuses, {len(already_exist)} already exist",
        "created": created,
        "already_exist": already_exist,
        "errors": errors
    }
