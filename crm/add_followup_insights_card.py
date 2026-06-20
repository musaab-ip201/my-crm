"""
Add Follow-Up Insights card to dashboard if missing
"""

import frappe
import json


def add_followup_insights_card():
	"""Add Follow-Up Insights card to the dashboard if it doesn't exist"""
	
	print("\n=== Adding Follow-Up Insights Card ===\n")
	
	# Get current layout
	layout = frappe.db.get_value("CRM Dashboard", "Manager Dashboard", "layout")
	
	if not layout:
		print("❌ Dashboard not found")
		return
	
	layout_data = json.loads(layout)
	
	# Check if followup_insights already exists
	has_followup = any(item.get('name') == 'followup_insights' for item in layout_data)
	
	if has_followup:
		print("✓ Follow-Up Insights card already exists in layout")
		return
	
	print("Adding Follow-Up Insights card...")
	
	# Find a good position for the card
	# Place it after the number charts, before the big charts
	# Look for a spot around y=3 or y=6
	
	# Find the highest Y position in the first row (y < 5)
	first_row_max_x = 0
	for item in layout_data:
		item_layout = item.get('layout', {})
		if item_layout.get('y', 0) < 5:
			item_right = item_layout.get('x', 0) + item_layout.get('w', 0)
			first_row_max_x = max(first_row_max_x, item_right)
	
	# If there's space in first row, use it; otherwise create new row
	if first_row_max_x <= 12:
		x_pos = first_row_max_x
		y_pos = 0
	else:
		# Find next available row
		max_y = 0
		for item in layout_data:
			item_layout = item.get('layout', {})
			item_bottom = item_layout.get('y', 0) + item_layout.get('h', 0)
			if item_bottom < 15:  # Only consider top section
				max_y = max(max_y, item_bottom)
		x_pos = 0
		y_pos = max_y
	
	# Create Follow-Up Insights card
	followup_card = {
		"name": "followup_insights",
		"type": "followup_insights",
		"layout": {
			"x": x_pos,
			"y": y_pos,
			"w": 20,      # Full width
			"h": 9,       # Height for 2 rows of cards
			"i": "followup_insights"
		}
	}
	
	print(f"\nCreating Follow-Up Insights card:")
	print(f"  x={followup_card['layout']['x']}, y={followup_card['layout']['y']}")
	print(f"  w={followup_card['layout']['w']}, h={followup_card['layout']['h']}")
	
	# Add to layout
	layout_data.append(followup_card)
	
	# Save updated layout
	frappe.db.set_value(
		"CRM Dashboard",
		"Manager Dashboard",
		"layout",
		json.dumps(layout_data)
	)
	
	frappe.db.commit()
	
	print("\n✓ Follow-Up Insights card added successfully!")
	print("\nNext steps:")
	print("1. Clear cache")
	print("2. Rebuild frontend")
	print("3. Restart services")
	print("4. Hard refresh browser")


if __name__ == "__main__":
	add_followup_insights_card()
