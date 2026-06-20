# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import time
import json

@frappe.whitelist()
def start_auto_dialer(lead_ids):
	"""Initialize auto dialer queue with selected leads"""
	if isinstance(lead_ids, str):
		lead_ids = json.loads(lead_ids)
	
	if not lead_ids:
		frappe.throw(_("No leads selected"), title=_("Invalid Input"))
	
	# Get leads with phone numbers
	valid_leads = []
	for lead_id in lead_ids:
		lead = frappe.get_doc("CRM Lead", lead_id)
		phone = lead.mobile_no or lead.phone
		if phone:
			valid_leads.append({
				"lead_id": lead_id,
				"lead_name": lead.lead_name,
				"phone": phone,
				"status": "Pending"
			})
	
	if not valid_leads:
		frappe.throw(_("None of the selected leads have phone numbers"), title=_("No Valid Leads"))
	
	# Create queue document
	queue_doc = frappe.get_doc({
		"doctype": "CRM Auto Dialer Queue",
		"user": frappe.session.user,
		"status": "Active",
		"total_leads": len(valid_leads),
		"completed_leads": 0,
		"failed_leads": 0,
		"leads": json.dumps(valid_leads)
	})
	queue_doc.insert(ignore_permissions=True)
	frappe.db.commit()
	
	return {
		"success": True,
		"queue_id": queue_doc.name,
		"total_leads": len(valid_leads),
		"skipped_leads": len(lead_ids) - len(valid_leads)
	}


@frappe.whitelist()
def get_queue_status(queue_id):
	"""Get current status of auto dialer queue"""
	if not frappe.db.exists("CRM Auto Dialer Queue", queue_id):
		frappe.throw(_("Queue not found"), title=_("Invalid Queue"))
	
	queue = frappe.get_doc("CRM Auto Dialer Queue", queue_id)
	leads = json.loads(queue.leads) if isinstance(queue.leads, str) else queue.leads
	
	return {
		"queue_id": queue.name,
		"status": queue.status,
		"total_leads": queue.total_leads,
		"completed_leads": queue.completed_leads,
		"failed_leads": queue.failed_leads,
		"current_index": queue.current_index or 0,
		"leads": leads,
		"modified": queue.modified
	}


@frappe.whitelist()
def pause_auto_dialer(queue_id):
	"""Pause the auto dialer"""
	frappe.db.set_value("CRM Auto Dialer Queue", queue_id, "status", "Paused")
	frappe.db.commit()
	return {"success": True, "status": "Paused"}


@frappe.whitelist()
def resume_auto_dialer(queue_id):
	"""Resume the auto dialer"""
	frappe.db.set_value("CRM Auto Dialer Queue", queue_id, "status", "Active")
	frappe.db.commit()
	return {"success": True, "status": "Active"}


@frappe.whitelist()
def stop_auto_dialer(queue_id):
	"""Stop the auto dialer"""
	frappe.db.set_value("CRM Auto Dialer Queue", queue_id, "status", "Stopped")
	frappe.db.commit()
	return {"success": True, "status": "Stopped"}


@frappe.whitelist()
def restart_auto_dialer(queue_id):
	"""Restart the auto dialer from the beginning or from where it left off"""
	queue = frappe.get_doc("CRM Auto Dialer Queue", queue_id)
	leads = json.loads(queue.leads) if isinstance(queue.leads, str) else queue.leads
	
	# Find first pending or failed lead
	restart_index = None
	for i, lead in enumerate(leads):
		if lead.get("status") in ["Pending", "Failed"]:
			restart_index = i
			break
	
	if restart_index is None:
		# All leads completed, restart from beginning
		restart_index = 0
		for lead in leads:
			lead["status"] = "Pending"
			lead.pop("ref_id", None)
			lead.pop("call_id", None)
			lead.pop("error", None)
		queue.completed_leads = 0
		queue.failed_leads = 0
	
	queue.current_index = restart_index - 1  # Will be incremented in process_next_call
	queue.status = "Active"
	queue.leads = json.dumps(leads)
	queue.save(ignore_permissions=True)
	frappe.db.commit()
	
	return {"success": True, "status": "Active", "restart_index": restart_index}


@frappe.whitelist()
def process_next_call(queue_id, current_call_status=None, lead_index=None, delay=0):
	"""Process next call in queue"""
	from crm.integrations.tata_tele.handler import make_a_call
	
	queue = frappe.get_doc("CRM Auto Dialer Queue", queue_id)
	leads = json.loads(queue.leads) if isinstance(queue.leads, str) else queue.leads
	
	if queue.status not in ["Active", "Paused"]:
		return {"success": False, "message": "Queue is not active"}
	
	# All statuses that mean the call is finished
	TERMINAL_COMPLETED = {"Completed"}
	TERMINAL_FAILED = {
		"Failed", "No Answer", "Busy", "Canceled",
		"Not received by seller", "Call not receive by agent",
	}
	ALL_TERMINAL = TERMINAL_COMPLETED | TERMINAL_FAILED

	# Update current call status if provided
	target_index = int(lead_index) if lead_index is not None else queue.current_index
	if current_call_status and target_index is not None and target_index >= 0 and target_index < len(leads):
		current_lead = leads[target_index]
		old_status = current_lead.get("status")
		if isinstance(current_call_status, dict):
			raw_status = current_call_status.get("status", "Completed")
			current_lead["call_log_id"] = current_call_status.get("call_log_id")
		else:
			raw_status = current_call_status
		
		# Store the original CRM status for tooltip/debug, but normalize for display
		current_lead["crm_status"] = raw_status
		if raw_status in TERMINAL_COMPLETED:
			current_lead["status"] = "Completed"
		elif raw_status in TERMINAL_FAILED:
			current_lead["status"] = "Failed"
		else:
			current_lead["status"] = raw_status
		
		# Count stats ONLY if it was previously non-terminal to avoid duplicate inflations
		if old_status not in ALL_TERMINAL:
			if current_lead["status"] == "Completed":
				queue.completed_leads += 1
			elif current_lead["status"] == "Failed":
				queue.failed_leads += 1
	
	# Always scan from the beginning to find the FIRST un-dialed Pending lead
	next_index = 0
	
	while next_index < len(leads) and leads[next_index].get("status") not in ["Pending"]:
		frappe.logger().info(f"[AUTO DIALER] Skipping index {next_index} because its status is {leads[next_index].get('status')}")
		next_index += 1
	
	if next_index >= len(leads):
		queue.status = "Completed"
		queue.leads = json.dumps(leads)
		queue.save(ignore_permissions=True)
		frappe.db.commit()
		return {"success": True, "completed": True, "message": "All calls completed"}
	
	# Check if paused
	if queue.status == "Paused":
		queue.current_index = next_index
		queue.leads = json.dumps(leads)
		queue.save(ignore_permissions=True)
		frappe.db.commit()
		return {"success": True, "paused": True, "message": "Queue is paused"}

	# SAVE before sleeping to prevent DocumentModified errors
	queue.current_index = next_index
	queue.leads = json.dumps(leads)
	queue.save(ignore_permissions=True)
	frappe.db.commit()
	
	# If delayed by webhook, pause the worker execution
	if delay and int(delay) > 0:
		frappe.logger().info(f"[AUTO DIALER] Sleeping for {delay} seconds before dialing next index {next_index}")
		time.sleep(int(delay))
		
		# RELOAD after sleeping in case user paused or modified the queue via UI
		queue.reload()
		leads = json.loads(queue.leads) if isinstance(queue.leads, str) else queue.leads
		
		if queue.status not in ["Active"]:
			return {"success": False, "message": f"Queue status changed to {queue.status} during sleep"}
	
	# Make the call
	next_lead = leads[next_index]
	
	lead_doc = frappe.get_doc("CRM Lead", next_lead["lead_id"])
	
	try:
		result = make_a_call(next_lead["phone"])
		next_lead["status"] = "Calling"
		next_lead["ref_id"] = result.get("ref_id")
		next_lead["call_id"] = result.get("call_id")
		
		queue.current_index = next_index
		queue.leads = json.dumps(leads)
		queue.save(ignore_permissions=True)
		frappe.db.commit()
		
		return {
			"success": True,
			"lead": {
				"lead_id": next_lead["lead_id"],
				"lead_name": next_lead["lead_name"],
				"phone": next_lead["phone"],
				"ref_id": result.get("ref_id"),
				"call_id": result.get("call_id")
			},
			"current_index": next_index,
			"total": len(leads)
		}
	except Exception as e:
		next_lead["status"] = "Failed"
		next_lead["error"] = str(e)
		queue.failed_leads += 1
		queue.current_index = next_index
		queue.leads = json.dumps(leads)
		queue.save(ignore_permissions=True)
		frappe.db.commit()
		
		frappe.log_error(frappe.get_traceback(), f"Auto Dialer Call Failed: {next_lead['lead_id']}")
		
		# Auto continue even if this specific call failed synchronously
		frappe.enqueue(
			"crm.integrations.tata_tele.auto_dialer.process_next_call",
			queue_id=queue.name,
			delay=int(delay) if delay else 5,
			queue="short",
			timeout=300,
			now=False,
			enqueue_after_commit=True
		)
		
		return {
			"success": False,
			"error": str(e),
			"lead": next_lead,
			"current_index": next_index,
			"total": len(leads)
		}
