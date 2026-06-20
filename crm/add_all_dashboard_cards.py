#!/usr/bin/env python3
"""
Add missing dashboard cards
Run: bench --site sitename.localhost execute crm.add_all_dashboard_cards.add_cards
"""

import frappe
import json

def add_cards():
    print("\n" + "="*60)
    print("ADDING DASHBOARD CARDS")
    print("="*60)
    
    try:
        # Get the dashboard
        dashboard = frappe.get_doc("CRM Dashboard", "Manager Dashboard")
        layout = json.loads(dashboard.layout or "[]")
        
        # Check which cards are missing
        card_names = [item.get("name") for item in layout]
        
        print(f"\nCurrent cards: {len(card_names)}")
        
        cards_added = 0
        
        # Fresh Leads card
        if "fresh_leads" not in card_names:
            layout.append({
                "name": "fresh_leads",
                "type": "number_chart",
                "tooltip": "Leads created today",
                "layout": {"x": 4, "y": 2, "w": 4, "h": 3, "i": "fresh_leads"}
            })
            print("✓ Added Fresh Leads card")
            cards_added += 1
        else:
            print("✓ Fresh Leads card already exists")
        
        # Call Insights card
        if "call_insights" not in card_names:
            layout.append({
                "name": "call_insights",
                "type": "custom",
                "tooltip": "Call center insights and statistics",
                "layout": {"x": 0, "y": 41, "w": 20, "h": 10, "i": "call_insights"}
            })
            print("✓ Added Call Insights card")
            cards_added += 1
        else:
            print("✓ Call Insights card already exists")
        
        # Follow-Up Insights card
        if "followup_insights" not in card_names:
            layout.append({
                "name": "followup_insights",
                "type": "custom",
                "tooltip": "Follow-up status tracking",
                "layout": {"x": 0, "y": 51, "w": 20, "h": 10, "i": "followup_insights"}
            })
            print("✓ Added Follow-Up Insights card")
            cards_added += 1
        else:
            print("✓ Follow-Up Insights card already exists")
        
        # Save if cards were added
        if cards_added > 0:
            dashboard.layout = json.dumps(layout)
            dashboard.save(ignore_permissions=True)
            frappe.db.commit()
            print(f"\n✓ Successfully added {cards_added} card(s)")
            print(f"  Total cards now: {len(layout)}")
        else:
            print("\n✓ All cards already exist")
        
        print("\n" + "="*60)
        print("NEXT STEPS:")
        print("="*60)
        print("1. bench --site sitename.localhost clear-cache")
        print("2. bench build --app crm")
        print("3. bench restart")
        print("4. Hard refresh browser (Ctrl + Shift + R)")
        print()
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add_cards()
