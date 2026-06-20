# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re

from crm.integrations.api import get_contact_by_phone_number
from crm.utils import seconds_to_duration


def _get_agent_by_number(number):
	"""Match last 10 digits of number against Smartflo Agent Mapping → return user email."""
	if not number:
		return None
	digits = "".join(ch for ch in str(number) if ch.isdigit())
	last10 = digits[-10:] if len(digits) >= 10 else digits
	if not last10:
		return None
	try:
		rows = frappe.db.sql(
			"SELECT user, agent_number FROM `tabSmartflo Agent Mapping`",
			as_dict=True,
		)
		for m in rows:
			stored = "".join(ch for ch in (m.get("agent_number") or "") if ch.isdigit())
			stored10 = stored[-10:] if len(stored) >= 10 else stored
			if last10 == stored10:
				return m["user"]
	except Exception:
		frappe.log_error(frappe.get_traceback(), "Agent mapping lookup failed in CRMCallLog")
	return None


class CRMCallLog(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.core.doctype.dynamic_link.dynamic_link import DynamicLink
		from frappe.types import DF

		caller: DF.Link | None
		disconnect_reason: DF.SmallText | None
		duration: DF.Duration | None
		end_time: DF.Datetime | None
		id: DF.Data | None
		links: DF.Table[DynamicLink]
		medium: DF.Data | None
		note: DF.Link | None
		receiver: DF.Link | None
		recording_url: DF.Text | None
		reference_docname: DF.DynamicLink | None
		reference_doctype: DF.Link | None
		start_time: DF.Datetime | None
		status: DF.Literal["Initiated", "Ringing", "In Progress", "Completed", "Failed", "Busy", "Call not receive by agent", "Call not receive by agent (Over Smartphone)", "Not received by seller"]
		telephony_medium: DF.Literal["", "Manual", "Twilio", "Exotel", "Tata Tele"]
		to: DF.Data
		type: DF.Literal["Incoming", "Outgoing"]
	# end: auto-generated types
	def after_insert(self):
		self._auto_set_receiver()
		self._auto_set_caller_receiver_names()

	def before_save(self):
		self._auto_set_receiver()
		self._auto_set_caller_receiver_names()

	def _auto_set_receiver(self):
		"""If incoming call has no receiver, look up agent by 'to' number in Smartflo Agent Mapping."""
		if self.type != "Incoming" or self.receiver:
			return
		to_number = getattr(self, "to", None) or frappe.db.get_value("CRM Call Log", self.name, "to")
		if not to_number:
			return
		user = _get_agent_by_number(to_number)
		if user:
			self.receiver = user
			frappe.logger().info(f"[CRM CALL LOG] Auto-set receiver={user} for {self.name} (to={to_number})")
			frappe.logger().info(f"[CRM CALL LOG] Auto-set receiver={user} for {self.name} (to={to_number})")

	def _auto_set_caller_receiver_names(self):
		"""Automatically set proper caller and receiver names for export compatibility"""
		try:
			if self.type == "Incoming":
				# For incoming calls: set caller name from contact lookup
				if not self.caller:
					contact = get_contact_by_phone_number(self.get("from"))
					if contact and contact.get("full_name"):
						self.caller = contact.get("full_name")
					elif self.get("from"):
						self.caller = self.get("from")
				
				# DON'T convert receiver User ID to name here - keep it as User ID for system functionality
				# The as_dict() method will handle the conversion for export only
						
			elif self.type == "Outgoing":
				# DON'T convert caller User ID to name here - keep it as User ID for system functionality  
				# The as_dict() method will handle the conversion for export only
				
				# For outgoing calls: set receiver name from contact lookup
				if not self.receiver:
					contact = get_contact_by_phone_number(self.get("to"))
					if contact and contact.get("full_name"):
						self.receiver = contact.get("full_name")
					elif self.get("to"):
						self.receiver = self.get("to")
						
		except Exception as e:
			frappe.logger().error(f"Error auto-setting caller/receiver names for {self.name}: {str(e)}")
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
				"label": "Call Start",
				"type": "Datetime",
				"key": "start_time",
				"width": "10rem",
			},
			{
				"label": "Call End",
				"type": "Datetime",
				"key": "end_time",
				"width": "10rem",
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
				"label": "Disconnect Reason",
				"type": "Small Text",
				"key": "disconnect_reason",
				"width": "12rem",
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
			"start_time",
			"end_time",
			"from",
			"to",
			"note",
			"disconnect_reason",
			"recording_url",
			"reference_doctype",
			"reference_docname",
			"creation",
		]
		return {"columns": columns, "rows": rows}

	@staticmethod
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
    
	def validate(self):
		self.from_ = self.validate_phone(getattr(self, "from"), "From")
		setattr(self, "from", self.from_)
		self.to = self.validate_phone(self.to, "To")
		if self.from_ and self.to and self.from_ == self.to:
			frappe.throw("From and To numbers cannot be the same")
		# self.validate_duration()

	def before_export(self, doc):
		"""Populate caller information for incoming calls before export"""
		if doc.get("type") == "Incoming" and not doc.get("caller"):
			# Get contact information from phone number
			contact = get_contact_by_phone_number(doc.get("from"))
			if contact and contact.get("full_name"):
				doc["caller"] = contact.get("full_name")
			else:
				doc["caller"] = doc.get("from", "Unknown")

	def as_dict(self, no_nulls=False, no_default_fields=False):
		"""Override as_dict to include proper caller and receiver names for export"""
		data = super().as_dict(no_nulls=no_nulls, no_default_fields=no_default_fields)
		
		if data.get("type") == "Incoming":
			# For incoming calls: populate caller field with contact name from 'from' number
			if not data.get("caller"):
				contact = get_contact_by_phone_number(data.get("from"))
				if contact and contact.get("full_name"):
					data["caller"] = contact.get("full_name")
				elif data.get("from"):
					data["caller"] = data.get("from")
			
			# For incoming calls: replace receiver User ID with user's full name
			if data.get("receiver"):
				try:
					receiver_name = frappe.db.get_value("User", data.get("receiver"), "full_name")
					if receiver_name:
						data["receiver"] = receiver_name
				except Exception:
					pass  # Keep original receiver value if lookup fails
					
		elif data.get("type") == "Outgoing":
			# For outgoing calls: replace caller User ID with user's full name
			if data.get("caller"):
				try:
					caller_name = frappe.db.get_value("User", data.get("caller"), "full_name")
					if caller_name:
						data["caller"] = caller_name
				except Exception:
					pass  # Keep original caller value if lookup fails
			
			# For outgoing calls: populate receiver field with contact name from 'to' number
			if not data.get("receiver"):
				contact = get_contact_by_phone_number(data.get("to"))
				if contact and contact.get("full_name"):
					data["receiver"] = contact.get("full_name")
				elif data.get("to"):
					data["receiver"] = data.get("to")
		
		return data

	@staticmethod
	def get_list_data(data):
		"""Process list data to include proper caller and receiver names"""
		processed_data = []
		for item in data:
			processed_item = item.copy()
			
			if item.get("type") == "Incoming":
				# For incoming calls: populate caller field with contact name
				if not item.get("caller"):
					contact = get_contact_by_phone_number(item.get("from"))
					if contact and contact.get("full_name"):
						processed_item["caller"] = contact.get("full_name")
					elif item.get("from"):
						processed_item["caller"] = item.get("from")
				
				# For incoming calls: replace receiver User ID with user's full name
				if item.get("receiver"):
					try:
						receiver_name = frappe.db.get_value("User", item.get("receiver"), "full_name")
						if receiver_name:
							processed_item["receiver"] = receiver_name
					except Exception:
						pass
						
			elif item.get("type") == "Outgoing":
				# For outgoing calls: replace caller User ID with user's full name
				if item.get("caller"):
					try:
						caller_name = frappe.db.get_value("User", item.get("caller"), "full_name")
						if caller_name:
							processed_item["caller"] = caller_name
					except Exception:
						pass
				
				# For outgoing calls: populate receiver field with contact name
				if not item.get("receiver"):
					contact = get_contact_by_phone_number(item.get("to"))
					if contact and contact.get("full_name"):
						processed_item["receiver"] = contact.get("full_name")
					elif item.get("to"):
						processed_item["receiver"] = item.get("to")
			
			processed_data.append(processed_item)
		
		return processed_data
		

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
				"disconnect_reason",
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


@frappe.whitelist()
def get_agent_call_logs(user=None, call_type=None, status=None, from_date=None, to_date=None, limit=20, start=0):
	"""
	Fetch call logs for an agent — incoming (receiver=user) OR outgoing (caller=user).
	Supports type, status, date range filters.
	"""
	if not user:
		user = frappe.session.user

	conditions = ["(cl.caller = %(user)s OR cl.receiver = %(user)s)"]
	params = {"user": user, "limit": int(limit), "start": int(start)}

	if call_type:
		conditions.append("cl.type = %(call_type)s")
		params["call_type"] = call_type

	if status:
		conditions.append("cl.status = %(status)s")
		params["status"] = status

	if from_date and to_date:
		conditions.append("DATE(cl.creation) BETWEEN %(from_date)s AND %(to_date)s")
		params["from_date"] = from_date
		params["to_date"] = to_date

	where = " AND ".join(conditions)

	calls = frappe.db.sql(
		f"""
		SELECT cl.name, cl.caller, cl.receiver, cl.`from`, cl.`to`,
		       cl.duration, cl.start_time, cl.end_time, cl.status,
		       cl.type, cl.recording_url, cl.creation, cl.note,
		       cl.reference_doctype, cl.reference_docname
		FROM `tabCRM Call Log` cl
		WHERE {where}
		ORDER BY cl.creation DESC
		LIMIT %(limit)s OFFSET %(start)s
		""",
		params,
		as_dict=True,
	)

	return [parse_call_log(call) for call in calls] if calls else []


@frappe.whitelist()
def fix_all_call_log_names():
	"""
	Permanently fix all caller and receiver names in the database
	This is a one-time fix that updates the actual database records
	"""
	try:
		# Get all call logs that need fixing
		call_logs = frappe.db.sql("""
			SELECT name, type, caller, receiver, `from`, `to`
			FROM `tabCRM Call Log`
			ORDER BY creation DESC
		""", as_dict=True)
		
		updated_count = 0
		errors = []
		
		for log in call_logs:
			updates = {}
			
			if log.get("type") == "Incoming":
				# For incoming calls: fix caller and receiver
				
				# Fix caller (should be contact name from 'from' number)
				if not log.get("caller") or log.get("caller") in ['', None]:
					try:
						contact = get_contact_by_phone_number(log.get("from"))
						if contact and contact.get("full_name"):
							updates["caller"] = contact.get("full_name")
						elif log.get("from"):
							updates["caller"] = log.get("from")
					except Exception as e:
						errors.append(f"Error getting contact for {log['name']}: {str(e)}")
				
				# Fix receiver (convert User ID to user name if needed)
				if log.get("receiver"):
					try:
						# Check if receiver looks like a User ID (email or long string)
						receiver_val = str(log.get("receiver"))
						if "@" in receiver_val or len(receiver_val) > 25:
							user_name = frappe.db.get_value("User", log.get("receiver"), "full_name")
							if user_name and user_name != log.get("receiver"):
								updates["receiver"] = user_name
					except Exception as e:
						errors.append(f"Error getting user for {log['name']}: {str(e)}")
						
			elif log.get("type") == "Outgoing":
				# For outgoing calls: fix caller and receiver
				
				# Fix caller (convert User ID to user name if needed)
				if log.get("caller"):
					try:
						# Check if caller looks like a User ID (email or long string)
						caller_val = str(log.get("caller"))
						if "@" in caller_val or len(caller_val) > 25:
							user_name = frappe.db.get_value("User", log.get("caller"), "full_name")
							if user_name and user_name != log.get("caller"):
								updates["caller"] = user_name
					except Exception as e:
						errors.append(f"Error getting user for {log['name']}: {str(e)}")
				
				# Fix receiver (should be contact name from 'to' number)
				if not log.get("receiver") or log.get("receiver") in ['', None]:
					try:
						contact = get_contact_by_phone_number(log.get("to"))
						if contact and contact.get("full_name"):
							updates["receiver"] = contact.get("full_name")
						elif log.get("to"):
							updates["receiver"] = log.get("to")
					except Exception as e:
						errors.append(f"Error getting contact for {log['name']}: {str(e)}")
			
			# Apply updates if any
			if updates:
				try:
					# Use frappe.db.set_value for safer updates
					for field, value in updates.items():
						frappe.db.set_value("CRM Call Log", log['name'], field, value)
					updated_count += 1
				except Exception as e:
					errors.append(f"Error updating {log['name']}: {str(e)}")
		
		# Commit all changes
		frappe.db.commit()
		
		result = {
			"success": True,
			"message": f"Successfully updated {updated_count} call log records",
			"updated_count": updated_count,
			"total_processed": len(call_logs),
			"errors": errors[:10] if errors else []  # Limit errors to first 10
		}
		
		return result
		
	except Exception as e:
		frappe.db.rollback()
		return {
			"success": False,
			"message": f"Error fixing call log names: {str(e)}",
			"updated_count": 0,
			"errors": [str(e)]
		}


@frappe.whitelist()
def update_call_log_names_for_export():
	"""
	Update caller and receiver fields with proper names for export
	This should be called before exporting to ensure names are populated
	"""
	# Get all call logs that need name updates
	call_logs = frappe.get_all(
		"CRM Call Log",
		fields=["name", "type", "caller", "receiver", "from", "to"],
		filters={}
	)
	
	updated_count = 0
	
	for log in call_logs:
		updates = {}
		
		if log.get("type") == "Incoming":
			# Update caller field with contact name if empty
			if not log.get("caller"):
				contact = get_contact_by_phone_number(log.get("from"))
				if contact and contact.get("full_name"):
					updates["caller"] = contact.get("full_name")
				elif log.get("from"):
					updates["caller"] = log.get("from")
			
			# Update receiver field with user name if it's a User ID
			if log.get("receiver"):
				try:
					# Check if receiver is a User ID (email format)
					if "@" in str(log.get("receiver")) or len(str(log.get("receiver"))) > 20:
						receiver_name = frappe.db.get_value("User", log.get("receiver"), "full_name")
						if receiver_name:
							updates["receiver"] = receiver_name
				except Exception:
					pass
					
		elif log.get("type") == "Outgoing":
			# Update caller field with user name if it's a User ID
			if log.get("caller"):
				try:
					# Check if caller is a User ID (email format)
					if "@" in str(log.get("caller")) or len(str(log.get("caller"))) > 20:
						caller_name = frappe.db.get_value("User", log.get("caller"), "full_name")
						if caller_name:
							updates["caller"] = caller_name
				except Exception:
					pass
			
			# Update receiver field with contact name if empty
			if not log.get("receiver"):
				contact = get_contact_by_phone_number(log.get("to"))
				if contact and contact.get("full_name"):
					updates["receiver"] = contact.get("full_name")
				elif log.get("to"):
					updates["receiver"] = log.get("to")
		
		# Apply updates if any
		if updates:
			frappe.db.set_value("CRM Call Log", log.get("name"), updates)
			updated_count += 1
	
	frappe.db.commit()
	
	return {
		"message": f"Updated {updated_count} call log records with proper names",
		"updated_count": updated_count
	}


@frappe.whitelist()
def export_call_logs_with_names(filters=None, file_type="Excel"):
	"""
	Custom export function for CRM Call Log that includes proper caller and receiver names
	"""
	import io
	import csv
	from frappe.utils.xlsxutils import make_xlsx
	from frappe.desk.utils import provide_binary_file
	
	# Get call logs with filters
	call_logs = frappe.get_list(
		"CRM Call Log",
		fields=[
			"name", "type", "status", "duration", "start_time", "end_time",
			"from", "to", "caller", "receiver", "disconnect_reason", 
			"telephony_medium", "creation"
		],
		filters=filters or {},
		order_by="creation desc"
	)
	
	# Process each call log to get proper names
	processed_logs = []
	for log in call_logs:
		processed_log = log.copy()
		
		if log.get("type") == "Incoming":
			# For incoming calls: get caller name from contact lookup
			if not log.get("caller"):
				contact = get_contact_by_phone_number(log.get("from"))
				if contact and contact.get("full_name"):
					processed_log["caller"] = contact.get("full_name")
				else:
					processed_log["caller"] = log.get("from", "Unknown")
			
			# For incoming calls: get receiver name from User
			if log.get("receiver"):
				try:
					receiver_name = frappe.db.get_value("User", log.get("receiver"), "full_name")
					if receiver_name:
						processed_log["receiver"] = receiver_name
				except Exception:
					pass
					
		elif log.get("type") == "Outgoing":
			# For outgoing calls: get caller name from User
			if log.get("caller"):
				try:
					caller_name = frappe.db.get_value("User", log.get("caller"), "full_name")
					if caller_name:
						processed_log["caller"] = caller_name
				except Exception:
					pass
			
			# For outgoing calls: get receiver name from contact lookup
			if not log.get("receiver"):
				contact = get_contact_by_phone_number(log.get("to"))
				if contact and contact.get("full_name"):
					processed_log["receiver"] = contact.get("full_name")
				else:
					processed_log["receiver"] = log.get("to", "Unknown")
		
		processed_logs.append(processed_log)
	
	# Define column headers
	headers = [
		"ID", "Caller", "Receiver", "Type", "Status", "Duration", 
		"From", "To", "Disconnect Reason", "Telephony Medium", 
		"Start Time", "End Time", "Creation"
	]
	
	# Define field mapping
	field_mapping = [
		"name", "caller", "receiver", "type", "status", "duration",
		"from", "to", "disconnect_reason", "telephony_medium",
		"start_time", "end_time", "creation"
	]
	
	if file_type.lower() == "excel":
		# Create Excel file
		data = [headers]
		for log in processed_logs:
			row = []
			for field in field_mapping:
				value = log.get(field, "")
				if field in ["start_time", "end_time", "creation"] and value:
					value = frappe.utils.format_datetime(value)
				elif field == "duration" and value:
					value = frappe.utils.format_duration(value)
				row.append(value)
			data.append(row)
		
		xlsx_file = make_xlsx(data, "Call Logs Export")
		provide_binary_file("CRM Call Log", "xlsx", xlsx_file.getvalue())
		
	else:
		# Create CSV file
		output = io.StringIO()
		writer = csv.writer(output)
		writer.writerow(headers)
		
		for log in processed_logs:
			row = []
			for field in field_mapping:
				value = log.get(field, "")
				if field in ["start_time", "end_time", "creation"] and value:
					value = frappe.utils.format_datetime(value)
				elif field == "duration" and value:
					value = frappe.utils.format_duration(value)
				row.append(value)
			writer.writerow(row)
		
		frappe.response["result"] = output.getvalue()
		frappe.response["type"] = "csv"
		frappe.response["doctype"] = "CRM Call Log"


def get_permission_query_conditions(user=None):
	"""
	Sales Users can only see call logs where they are the caller (outgoing)
	or the receiver (incoming). Managers and Admins see all.
	"""
	if not user:
		user = frappe.session.user

	if user == "Administrator":
		return ""

	roles = frappe.get_roles(user)
	if "System Manager" in roles or "Sales Manager" in roles:
		return ""

	# Sales User: show calls where they are caller OR receiver
	return f"(`tabCRM Call Log`.caller = {frappe.db.escape(user)} OR `tabCRM Call Log`.receiver = {frappe.db.escape(user)})"
