"""
Follow-up management functions
"""

import frappe
from frappe import _


def update_followup_statuses():
	"""
	Scheduled job to auto-update follow-up statuses based on dates.
	Runs every hour to check and update:
	- Planned → Pending (when date becomes today or past)
	- Pending → Missed (when date is past and not completed)
	"""
	
	today = frappe.utils.nowdate()
	
	# Update Planned to Pending (when follow-up date is today or past)
	frappe.db.sql("""
		UPDATE `tabCRM Lead`
		SET followup_status = 'Pending'
		WHERE followup_status = 'Planned'
		AND next_followup_date <= %(today)s
		AND next_followup_date IS NOT NULL
	""", {"today": today})
	
	# Update Pending to Missed (when follow-up date is past)
	frappe.db.sql("""
		UPDATE `tabCRM Lead`
		SET followup_status = 'Missed'
		WHERE followup_status = 'Pending'
		AND next_followup_date < %(today)s
		AND next_followup_date IS NOT NULL
	""", {"today": today})
	
	# Also catch any leads without status but with past follow-up dates
	frappe.db.sql("""
		UPDATE `tabCRM Lead`
		SET followup_status = 'Missed'
		WHERE (followup_status IS NULL OR followup_status = '')
		AND next_followup_date < %(today)s
		AND next_followup_date IS NOT NULL
	""", {"today": today})
	
	frappe.db.commit()
	
	frappe.logger().info("Follow-up statuses updated successfully")


@frappe.whitelist()
def mark_followup_done(lead_name):
	"""
	Mark a follow-up as done for a lead.
	Updates followup_status to 'Done' and sets last_followup_date.
	"""
	
	if not lead_name:
		frappe.throw(_("Lead name is required"))
	
	lead = frappe.get_doc("CRM Lead", lead_name)
	
	lead.followup_status = "Done"
	lead.last_followup_date = frappe.utils.now_datetime()
	lead.save(ignore_permissions=True)
	
	frappe.db.commit()
	
	return {
		"success": True,
		"message": _("Follow-up marked as done")
	}


@frappe.whitelist()
def reschedule_followup(lead_name, new_date, new_time=None, notes=None):
	"""
	Reschedule a follow-up for a lead.
	Updates next_followup_date, next_followup_time, and sets status to 'Rescheduled'.
	"""
	
	if not lead_name or not new_date:
		frappe.throw(_("Lead name and new date are required"))
	
	lead = frappe.get_doc("CRM Lead", lead_name)
	
	lead.next_followup_date = new_date
	if new_time:
		lead.next_followup_time = new_time
	if notes:
		lead.followup_notes = notes
	lead.followup_status = "Rescheduled"
	lead.save(ignore_permissions=True)
	
	frappe.db.commit()
	
	return {
		"success": True,
		"message": _("Follow-up rescheduled successfully")
	}


@frappe.whitelist()
def cancel_followup(lead_name, reason=None):
	"""
	Cancel a follow-up for a lead.
	Sets followup_status to 'Cancelled'.
	"""
	
	if not lead_name:
		frappe.throw(_("Lead name is required"))
	
	lead = frappe.get_doc("CRM Lead", lead_name)
	
	lead.followup_status = "Cancelled"
	if reason:
		lead.followup_notes = reason
	lead.save(ignore_permissions=True)
	
	frappe.db.commit()
	
	return {
		"success": True,
		"message": _("Follow-up cancelled")
	}
