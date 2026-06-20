"""
Add follow-up tracking fields to CRM Lead
"""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
	"""Add follow-up fields to CRM Lead doctype"""
	
	custom_fields = {
		"CRM Lead": [
			{
				"fieldname": "followup_section",
				"label": "Follow-Up Details",
				"fieldtype": "Section Break",
				"insert_after": "status",
				"collapsible": 1,
			},
			{
				"fieldname": "next_followup_date",
				"label": "Next Follow-Up Date",
				"fieldtype": "Date",
				"insert_after": "followup_section",
			},
			{
				"fieldname": "next_followup_time",
				"label": "Follow-Up Time",
				"fieldtype": "Time",
				"insert_after": "next_followup_date",
			},
			{
				"fieldname": "column_break_followup",
				"fieldtype": "Column Break",
				"insert_after": "next_followup_time",
			},
			{
				"fieldname": "followup_status",
				"label": "Follow-Up Status",
				"fieldtype": "Select",
				"options": "\nPlanned\nPending\nDone\nMissed\nRescheduled\nCancelled",
				"insert_after": "column_break_followup",
				"default": "",
			},
			{
				"fieldname": "followup_notes",
				"label": "Follow-Up Notes",
				"fieldtype": "Small Text",
				"insert_after": "followup_status",
			},
			{
				"fieldname": "last_followup_date",
				"label": "Last Follow-Up Date",
				"fieldtype": "Datetime",
				"insert_after": "followup_notes",
				"read_only": 1,
			},
		]
	}
	
	create_custom_fields(custom_fields, update=True)
	
	frappe.db.commit()
	
	print("Follow-up fields added to CRM Lead successfully")
