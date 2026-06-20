# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from crm.integrations.api import get_contact_by_phone_number
from crm.utils import seconds_to_duration


class CRMCallLog(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.core.doctype.dynamic_link.dynamic_link import DynamicLink
		from frappe.types import DF

		caller: DF.Link | None
		duration: DF.Duration | None
		end_time: DF.Datetime | None
		id: DF.Data | None
		links: DF.Table[DynamicLink]
		medium: DF.Data | None
		note: DF.Link | None
		receiver: DF.Link | None
		recording_url: DF.Data | None
		reference_docname: DF.DynamicLink | None
		reference_doctype: DF.Link | None
		start_time: DF.Datetime | None
		status: DF.Literal["Initiated", "Ringing", "In Progress", "Completed", "Failed", "Busy", "No Answer", "Queued", "Canceled"]
		telephony_medium: DF.Literal["", "Manual", "Twilio", "Exotel", "Tata Tele"]
		to: DF.Data
		type: DF.Literal["Incoming", "Outgoing"]
	# end: auto-generated types
# call log form validation updated at 06-04-2026
	# def validate_duration(self):
	# 		if self.duration:
	# 			duration_str = str(self.duration)
	# 			if not re.fullmatch(r"\d{1,2}:\d{2}:\d{2}", self.duration):
	# 				frappe.throw("Duration must be in HH:MM:SS format")
	# 			h, m, s = map(int, duration_str.split(":"))
	# 			self.duration = h * 3600 + m * 60 + s

	def validate(self):
		self.from_ = self.validate_phone(getattr(self, "from"), "From")
		setattr(self, "from", self.from_)
		self.to = self.validate_phone(self.to, "To")
		if self.from_ and self.to and self.from_ == self.to:
			frappe.throw("From and To numbers cannot be the same")
		# self.validate_duration()
		

	def validate_phone(self, number, field_name):
		if not number:
			return number
		number = re.sub(r"\D", "", number)
		if number.startswith("91") and len(number) > 10:
			number = number[2:]
		if not re.fullmatch(r"[6-9]\d{9}", number):
			frappe.throw(f"{field_name} must be a valid 10-digit Indian mobile number")
		if number in ["0000000000", "1111111111", "1234567890"]:
			frappe.throw(f"{field_name} cannot be a dummy number")
		return number
# --------------------------
	def on_update(self):
		"""Auto-create follow-up when call is completed"""
		if self.has_value_changed("status") and self.status == "Completed":
			self.create_auto_followup()
	
	def create_auto_followup(self):
		"""Create automatic follow-up for completed calls"""
		try:
			# Only create follow-up if linked to a lead
			lead_name = None
			
			# Check reference_docname
			if self.reference_doctype == "CRM Lead" and self.reference_docname:
				lead_name = self.reference_docname
			
			# Check links
			if not lead_name and self.links:
				for link in self.links:
					if link.link_doctype == "CRM Lead":
						lead_name = link.link_name
						break
			
			if not lead_name:
				return  # No lead linked, skip
			
			# Get lead
			lead = frappe.get_doc("CRM Lead", lead_name)
			
			# Only create follow-up if one doesn't already exist
			if lead.next_followup_date:
				return  # Follow-up already set manually
			
			# Determine follow-up date based on call type and duration
			followup_days = 1  # Default: next day
			followup_time = "10:00:00"  # Default: 10 AM
			followup_notes = ""
			
			if self.type == "Incoming":
				# Inbound call - follow up next day
				followup_days = 1
				followup_notes = "Follow-up after inbound call"
			elif self.type == "Outgoing":
				# Outbound call
				if self.duration and int(self.duration) > 60:
					# Long call (>1 min) - follow up in 3 days
					followup_days = 3
					followup_notes = "Follow-up after successful call"
				else:
					# Short call or no answer - follow up tomorrow
					followup_days = 1
					followup_notes = "Follow-up - previous call was brief"
			
			# Set follow-up
			lead.next_followup_date = frappe.utils.add_days(frappe.utils.nowdate(), followup_days)
			lead.next_followup_time = followup_time
			lead.followup_status = "Planned"
			lead.followup_notes = followup_notes
			lead.save(ignore_permissions=True)
			
			frappe.logger().info(f"Auto follow-up created for lead {lead_name} after call {self.name}")
			
		except Exception as e:
			frappe.log_error(f"Error creating auto follow-up for call {self.name}: {str(e)}", "Auto Follow-Up Error")

	@staticmethod
	def default_list_data():
		columns = [
			{
				"label": "Caller",
				"type": "Link",
				"key": "caller",
				"options": "User",
				"width": "9rem",
			},
			{
				"label": "Receiver",
				"type": "Link",
				"key": "receiver",
				"options": "User",
				"width": "9rem",
			},
			{
				"label": "Type",
				"type": "Select",
				"key": "type",
				"width": "9rem",
			},
			{
				"label": "Status",
				"type": "Select",
				"key": "status",
				"width": "9rem",
			},
			{
				"label": "Duration",
				"type": "Duration",
				"key": "duration",
				"width": "6rem",
			},
			{
				"label": "From (number)",
				"type": "Data",
				"key": "from",
				"width": "9rem",
			},
			{
				"label": "To (number)",
				"type": "Data",
				"key": "to",
				"width": "9rem",
			},
			{
				"label": "Created On",
				"type": "Datetime",
				"key": "creation",
				"width": "8rem",
			},
		]
		rows = [
			"name",
			"caller",
			"receiver",
			"type",
			"status",
			"duration",
			"from",
			"to",
			"note",
			"recording_url",
			"reference_doctype",
			"reference_docname",
			"creation",
		]
		return {"columns": columns, "rows": rows}

	def parse_list_data(calls):
		return [parse_call_log(call) for call in calls] if calls else []

	def has_link(self, doctype, name):
		for link in self.links:
			if link.link_doctype == doctype and link.link_name == name:
				return True

	def link_with_reference_doc(self, reference_doctype, reference_name):
		if self.has_link(reference_doctype, reference_name):
			return

		self.append("links", {"link_doctype": reference_doctype, "link_name": reference_name})


def parse_call_log(call):
	try:
		call["show_recording"] = False
		call["_duration"] = seconds_to_duration(call.get("duration"))
		if call.get("type") == "Incoming":
			call["activity_type"] = "incoming_call"
			contact = get_contact_by_phone_number(call.get("from"))
			receiver = [None, None]
			if call.get("receiver"):
				receiver_data = frappe.db.get_values("User", call.get("receiver"), ["full_name", "user_image"])
				if receiver_data:
					receiver = receiver_data[0]
			call["_caller"] = {
				"label": contact.get("full_name", "Unknown"),
				"image": contact.get("image"),
			}
			call["_receiver"] = {
				"label": receiver[0] or "Unknown",
				"image": receiver[1],
			}
		elif call.get("type") == "Outgoing":
			call["activity_type"] = "outgoing_call"
			contact = get_contact_by_phone_number(call.get("to"))
			caller = [None, None]
			if call.get("caller"):
				caller_data = frappe.db.get_values("User", call.get("caller"), ["full_name", "user_image"])
				if caller_data:
					caller = caller_data[0]
			call["_caller"] = {
				"label": caller[0] or frappe.session.user or "Unknown",
				"image": caller[1],
			}
			call["_receiver"] = {
				"label": contact.get("full_name", "Unknown"),
				"image": contact.get("image"),
			}

		return call
	except Exception as e:
		frappe.log_error(f"Error parsing call log {call.get('name')}: {str(e)}", "Parse Call Log Error")
		# Return minimal valid call data
		return {
			"name": call.get("name"),
			"show_recording": False,
			"_duration": "00:00",
			"activity_type": "outgoing_call",
			"_caller": {"label": "Unknown", "image": None},
			"_receiver": {"label": "Unknown", "image": None},
			**call
		}


@frappe.whitelist()
def get_call_log(name):
	# Check if call log exists
	if not frappe.db.exists("CRM Call Log", name):
		return None  # Return None instead of throwing error
	
	try:
		call = frappe.get_cached_doc(
			"CRM Call Log",
			name,
			fields=[
				"name",
				"caller",
				"receiver",
				"duration",
				"type",
				"status",
				"from",
				"to",
				"note",
				"recording_url",
				"reference_doctype",
				"reference_docname",
				"creation",
			],
		).as_dict()

		call = parse_call_log(call)
	except Exception as e:
		frappe.log_error(f"Error fetching call log {name}: {str(e)}", "Get Call Log Error")
		return None

	notes = []
	tasks = []

	if call.get("note"):
		note = frappe.get_cached_doc("FCRM Note", call.get("note")).as_dict()
		notes.append(note)

	if call.get("reference_doctype") and call.get("reference_docname"):
		if call.get("reference_doctype") == "CRM Lead":
			call["_lead"] = call.get("reference_docname")
		elif call.get("reference_doctype") == "CRM Deal":
			call["_deal"] = call.get("reference_docname")

	if call.get("links"):
		for link in call.get("links"):
			if link.get("link_doctype") == "CRM Task":
				task = frappe.get_cached_doc("CRM Task", link.get("link_name")).as_dict()
				tasks.append(task)
			elif link.get("link_doctype") == "FCRM Note":
				note = frappe.get_cached_doc("FCRM Note", link.get("link_name")).as_dict()
				notes.append(note)
			elif link.get("link_doctype") == "CRM Lead":
				call["_lead"] = link.get("link_name")
			elif link.get("link_doctype") == "CRM Deal":
				call["_deal"] = link.get("link_name")

	call["_tasks"] = tasks
	call["_notes"] = notes
	return call


@frappe.whitelist()
def create_lead_from_call_log(call_log, lead_details=None):
	lead = frappe.new_doc("CRM Lead")
	lead_details = frappe.parse_json(lead_details or "{}")

	if not lead_details.get("lead_owner"):
		lead_details["lead_owner"] = frappe.session.user
	if not lead_details.get("mobile_no"):
		lead_details["mobile_no"] = call_log.get("from") or ""
	if not lead_details.get("first_name"):
		lead_details["first_name"] = "Lead from call " + (
			lead_details.get("mobile_no") or call_log.get("name")
		)

	lead.update(lead_details)
	lead.save(ignore_permissions=True)

	# link call log with lead
	call_log = frappe.get_doc("CRM Call Log", call_log.get("name"))
	call_log.link_with_reference_doc("CRM Lead", lead.name)
	call_log.save(ignore_permissions=True)

	return lead.name