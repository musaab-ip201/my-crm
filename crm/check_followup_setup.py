"""
Check if follow-up fields are properly set up
"""

import frappe


def check_fields():
	"""Check if follow-up custom fields exist in CRM Lead"""
	
	print("\n=== Checking Follow-Up Custom Fields ===\n")
	
	required_fields = [
		"followup_section",
		"next_followup_date",
		"next_followup_time",
		"column_break_followup",
		"followup_status",
		"followup_notes",
		"last_followup_date",
	]
	
	missing_fields = []
	existing_fields = []
	
	for fieldname in required_fields:
		exists = frappe.db.exists("Custom Field", {
			"dt": "CRM Lead",
			"fieldname": fieldname
		})
		
		if exists:
			existing_fields.append(fieldname)
			print(f"✓ {fieldname} - EXISTS")
		else:
			missing_fields.append(fieldname)
			print(f"✗ {fieldname} - MISSING")
	
	print(f"\n{len(existing_fields)} fields exist, {len(missing_fields)} fields missing")
	
	if missing_fields:
		print("\nTo fix, run:")
		print("bench --site sitename.localhost migrate")
	else:
		print("\n✓ All follow-up fields are properly configured!")
	
	# Check if any leads have follow-up data
	print("\n=== Checking Follow-Up Data ===\n")
	
	leads_with_followup = frappe.db.sql("""
		SELECT COUNT(*) as count
		FROM `tabCRM Lead`
		WHERE next_followup_date IS NOT NULL
	""", as_dict=True)
	
	count = leads_with_followup[0].count if leads_with_followup else 0
	print(f"Leads with follow-up data: {count}")
	
	if count > 0:
		# Show sample data
		sample = frappe.db.sql("""
			SELECT name, next_followup_date, followup_status
			FROM `tabCRM Lead`
			WHERE next_followup_date IS NOT NULL
			LIMIT 5
		""", as_dict=True)
		
		print("\nSample leads with follow-ups:")
		for lead in sample:
			print(f"  - {lead.name}: {lead.next_followup_date} ({lead.followup_status or 'No status'})")
	
	return {
		"existing_fields": existing_fields,
		"missing_fields": missing_fields,
		"leads_with_followup": count
	}
