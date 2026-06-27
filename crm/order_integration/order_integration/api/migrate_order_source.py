"""
Migration script to populate order_source field for existing leads
"""

import frappe


@frappe.whitelist()
def migrate_leads_order_source():
    """
    Populate order_source field for all leads that don't have it
    This is a one-time migration for existing leads
    """
    print("\n" + "="*80)
    print("[ORDER_INTEGRATION] Migrating leads to populate order_source...")
    print("="*80 + "\n")
    
    try:
        # Get all leads without order_source
        leads = frappe.db.sql("""
            SELECT name, lead_name 
            FROM `tabCRM Lead` 
            WHERE order_source IS NULL OR order_source = ''
        """, as_dict=True)
        
        print(f"[ORDER_INTEGRATION] Found {len(leads)} leads without order_source")
        
        if len(leads) == 0:
            print("[ORDER_INTEGRATION] ✅ All leads already have order_source populated")
            return {
                "status": "success",
                "message": "All leads already migrated",
                "updated": 0
            }
        
        # Get the first (default) order source
        default_source = frappe.db.get_value(
            "Order Sync Source",
            order_by="creation asc",
            fieldname="name"
        )
        
        if not default_source:
            print("[ORDER_INTEGRATION] ⚠️ No Order Sync Source found!")
            return {
                "status": "error",
                "message": "No Order Sync Source configured",
                "updated": 0
            }
        
        print(f"[ORDER_INTEGRATION] Using default source: {default_source}")
        
        # Update all leads to use the default source
        frappe.db.sql("""
            UPDATE `tabCRM Lead` 
            SET order_source = %s 
            WHERE order_source IS NULL OR order_source = ''
        """, (default_source,))
        
        frappe.db.commit()
        
        print(f"[ORDER_INTEGRATION] ✅ Updated {len(leads)} leads with order_source")
        
        return {
            "status": "success",
            "message": f"Updated {len(leads)} leads",
            "updated": len(leads),
            "source": default_source
        }
        
    except Exception as e:
        print(f"[ORDER_INTEGRATION] ❌ Error during migration: {str(e)}")
        frappe.log_error(f"Migration error: {str(e)}", "Order Integration Migration")
        return {
            "status": "error",
            "message": str(e),
            "updated": 0
        }


print("[ORDER_INTEGRATION] ✅ migrate_order_source.py loaded")
