"""
Add Call Insights card to dashboard if missing
"""

import frappe
import json


def add_call_insights_card():
	"""Add Call Insights card to the dashboard if it doesn't exist"""
	
	print("\n=== Adding Call Insights Card ===\n")
	
	# Get current layout
	layout = frappe.db.get_value("CRM Dashboard", "Manager Dashboard", "layout")
	
	if not layout:
		print("❌ Dashboard not found")
		return
	
	layout_data = json.loads(layout)
	
	# Check if call_insights already exists
	has_call_insights = any(item.get('name') == 'call_insights' for item in layout_data)
	
	if has_call_insights:
		print("✓ Call Insights card already exists in layout")
		return
	
	print("Adding Call Insights card...")
	
	# Find the highest Y position to place the card below everything
	max_y = 0
	for item in layout_data:
		item_layout = item.get('layout', {})
		item_bottom = item_layout.get('y', 0) + item_layout.get('h', 0)
		max_y = max(max_y, item_bottom)
	
	# Create Call Insights card
	call_insights_card = {
		"name": "call_insights",
		"type": "call_insights",
		"layout": {
			"x": 0,
			"y": max_y,  # Place at the bottom
			"w": 20,     # Full width
			"h": 10,     # Height for call insights
			"minH": 10,
			"i": "call_insights"
		}
	}
	
	print(f"\nCreating Call Insights card:")
	print(f"  x={call_insights_card['layout']['x']}, y={call_insights_card['layout']['y']}")
	print(f"  w={call_insights_card['layout']['w']}, h={call_insights_card['layout']['h']}")
	
	# Add to layout
	layout_data.append(call_insights_card)
	
	# Save updated layout
	frappe.db.set_value(
		"CRM Dashboard",
		"Manager Dashboard",
		"layout",
		json.dumps(layout_data)
	)
	
	frappe.db.commit()
	
	print("\n✓ Call Insights card added successfully!")
	print("\nNext steps:")
	print("1. Clear cache: bench --site sitename.localhost clear-cache")
	print("2. Rebuild frontend: bench build --app crm")
	print("3. Restart: bench restart")
	print("4. Hard refresh browser (Ctrl + Shift + R)")


if __name__ == "__main__":
	add_call_insights_card()
