#!/usr/bin/env python3
"""
Add follow-up fields to CRM Lead if missing
Run: bench --site sitename.localhost execute crm.add_followup_fields.add_fields
"""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def add_fields():
    print("\n" + "="*60)
    print("ADDING FOLLOW-UP FIELDS TO CRM LEAD")
    print("="*60)
    
    try:
        # Check if fields already exist
        meta = frappe.get_meta("CRM Lead")
        existing_fields = [f.fieldname for f in meta.fields]
        
        required_fields = {
            "followup_status": "Select",
            "next_followup_date": "Date",
            "last_followup_date": "Date",
            "followup_notes": "Small Text"
        }
        
        print("\nChecking existing fields...")
        missing_fields = []
        for field, fieldtype in required_fields.items():
            if field in existing_fields:
                print(f"  ✓ {field} exists")
            else:
                print(f"  ✗ {field} MISSING")
                missing_fields.append(field)
        
        if not missing_fields:
            print("\n✓ All follow-up fields already exist!")
            return
        
        print(f"\nAdding {len(missing_fields)} missing field(s)...")
        
        # Define custom fields
        custom_fields = {
            "CRM Lead": []
        }
        
        if "followup_status" in missing_fields:
            custom_fields["CRM Lead"].append({
                "fieldname": "followup_status",
                "label": "Follow-up Status",
                "fieldtype": "Select",
                "options": "\nPlanned\nPending\nRescheduled\nCancelled\nDone\nMissed",
                "insert_after": "status",
                "in_list_view": 1,
                "in_standard_filter": 1,
            })
        
        if "next_followup_date" in missing_fields:
            custom_fields["CRM Lead"].append({
                "fieldname": "next_followup_date",
                "label": "Next Follow-up Date",
                "fieldtype": "Date",
                "insert_after": "followup_status",
                "in_list_view": 1,
                "in_standard_filter": 1,
            })
        
        if "last_followup_date" in missing_fields:
            custom_fields["CRM Lead"].append({
                "fieldname": "last_followup_date",
                "label": "Last Follow-up Date",
                "fieldtype": "Date",
                "insert_after": "next_followup_date",
            })
        
        if "followup_notes" in missing_fields:
            custom_fields["CRM Lead"].append({
                "fieldname": "followup_notes",
                "label": "Follow-up Notes",
                "fieldtype": "Small Text",
                "insert_after": "last_followup_date",
            })
        
        # Create the custom fields
        create_custom_fields(custom_fields, update=True)
        frappe.db.commit()
        
        print(f"\n✓ Successfully added {len(missing_fields)} field(s)")
        print("\nFields added:")
        for field in missing_fields:
            print(f"  - {field}")
        
        print("\n" + "="*60)
        print("NEXT STEPS:")
        print("="*60)
        print("1. bench --site sitename.localhost clear-cache")
        print("2. bench --site sitename.localhost migrate")
        print("3. bench restart")
        print()
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add_fields()
