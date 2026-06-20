#!/usr/bin/env python3
"""
Check current dashboard status
Run: bench --site sitename.localhost execute crm.check_dashboard_status.check
"""

import frappe
import json

def check():
    print("\n" + "="*60)
    print("DASHBOARD STATUS CHECK")
    print("="*60)
    
    # 1. Check dashboard layout
    print("\n1. Checking dashboard layout...")
    try:
        dashboard = frappe.get_doc("CRM Dashboard", "Manager Dashboard")
        layout = json.loads(dashboard.layout or "[]")
        card_names = [item.get("name") for item in layout]
        
        print(f"   Total cards: {len(card_names)}")
        print(f"   fresh_leads: {'YES' if 'fresh_leads' in card_names else 'NO'}")
        print(f"   call_insights: {'YES' if 'call_insights' in card_names else 'NO'}")
        print(f"   followup_insights: {'YES' if 'followup_insights' in card_names else 'NO'}")
        
        if "fresh_leads" not in card_names or "call_insights" not in card_names or "followup_insights" not in card_names:
            print("\n   ✗ MISSING CARDS - Need to add them!")
        else:
            print("\n   ✓ All cards exist in layout")
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # 2. Test backend functions
    print("\n2. Testing backend functions...")
    
    try:
        from crm.api.dashboard import get_fresh_leads
        result = get_fresh_leads("2024-01-01", "2024-12-31", "")
        print(f"   ✓ get_fresh_leads: {result.get('value', 0)} leads")
    except Exception as e:
        print(f"   ✗ get_fresh_leads: {e}")
    
    try:
        from crm.api.dashboard import get_call_insights
        result = get_call_insights("2024-01-01", "2024-12-31", "")
        print(f"   ✓ get_call_insights: {len(result.get('data', []))} metrics")
    except Exception as e:
        print(f"   ✗ get_call_insights: {e}")
    
    try:
        from crm.api.dashboard import get_followup_insights
        result = get_followup_insights("2024-01-01", "2024-12-31", "")
        print(f"   ✓ get_followup_insights: {result.get('total', 0)} total")
    except Exception as e:
        print(f"   ✗ get_followup_insights: {e}")
    
    # 3. Check follow-up fields in Lead
    print("\n3. Checking follow-up fields in CRM Lead...")
    try:
        meta = frappe.get_meta("CRM Lead")
        fields = [f.fieldname for f in meta.fields]
        
        required_fields = ["followup_status", "next_followup_date", "last_followup_date", "followup_notes"]
        for field in required_fields:
            if field in fields:
                print(f"   ✓ {field} exists")
            else:
                print(f"   ✗ {field} MISSING")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n" + "="*60)
    print("CHECK COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    check()
