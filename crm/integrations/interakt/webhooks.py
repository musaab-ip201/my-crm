"""
Interakt Webhook Handler
Handles incoming webhooks from Interakt for:
- Incoming messages
- Message status updates (delivered, read)
"""

import frappe
from frappe import _
import json


@frappe.whitelist(allow_guest=True)
def handle_webhook():
	"""
	Main webhook handler for Interakt events.
	Endpoint: /api/method/crm.integrations.interakt.webhooks.handle_webhook
	"""
	if getattr(frappe.local, "site", None) is None:
		frappe.logger().error("Interakt Webhook: frappe.local.site is None")
		return

	try:
		# Get webhook data
		data = frappe.request.get_data(as_text=True)
		webhook_data = json.loads(data) if data else frappe.local.form_dict
		
		# Log webhook for debugging
		frappe.logger().info(f"Interakt Webhook Received: {json.dumps(webhook_data, indent=2)}")
		
		# Get event type
		event_type = webhook_data.get("type")
		
		if event_type == "message_received":
			handle_message_received(webhook_data)
		elif event_type == "message_status_update":
			handle_status_update(webhook_data)
		else:
			frappe.logger().info(f"Unknown webhook type: {event_type}")
		
		return {"success": True, "message": "Webhook processed"}
		
	except Exception as e:
		frappe.log_error(
			title="Interakt Webhook Error",
			message=f"Error processing webhook: {str(e)}\nData: {frappe.request.get_data(as_text=True)}"
		)
		return {"success": False, "error": str(e)}


def handle_message_received(webhook_data):
	"""
	Handle incoming message from customer.
	
	Webhook format:
	{
		"type": "message_received",
		"data": {
			"customer": {
				"channel_phone_number": "917003705584",
				"traits": {"name": "John Doe", ...}
			},
			"message": {
				"id": "message-id",
				"message": "Hello!",
				"message_content_type": "Text",
				"media_url": null,
				"received_at_utc": "2022-06-03T05:57:57.359000"
			}
		}
	}
	"""
	try:
		# Interakt sometimes wraps the payload in "data", and sometimes doesn't
		data = webhook_data.get("data") or webhook_data
		customer = data.get("customer", {})
		message = data.get("message", {})
		
		# Extract phone number (varies between 'phone_number' and 'channel_phone_number')
		phone_number = customer.get("phone_number") or customer.get("channel_phone_number", "")
		if not phone_number:
			frappe.logger().error(f"No phone number in webhook: {json.dumps(webhook_data)}")
			return
		
		# Clean phone number (remove country code for matching)
		clean_phone = phone_number.lstrip("+")
		
		# Get default country code from settings
		settings = frappe.get_single("CRM Interakt Settings")
		default_country_code = settings.default_country_code or "+91"
		country_code_digits = default_country_code.lstrip("+")
		
		if clean_phone.startswith(country_code_digits):
			clean_phone = clean_phone[len(country_code_digits):]
		
		# Find lead/deal/contact by phone number
		reference_doctype, reference_docname = find_document_by_phone(clean_phone)
		
		if not reference_doctype:
			frappe.logger().error(f"WhatsApp Webhook Matching Failed: No document found for phone: {phone_number} (cleaned: {clean_phone})")
			return
		
		frappe.logger().info(f"WhatsApp Webhook Matched: {reference_doctype} {reference_docname} for phone: {phone_number}")
		
		# Extract message details
		message_id = message.get("id")
		message_text = message.get("message", "")
		content_type = message.get("message_content_type", "Text").lower()
		media_url = message.get("media_url")
		
		# Check if message already exists
		existing = frappe.db.exists("CRM WhatsApp Message", {"message_id": message_id})
		if existing:
			frappe.logger().info(f"Message {message_id} already exists")
			return
		
		# Create incoming message record
		doc = frappe.new_doc("CRM WhatsApp Message")
		doc.update({
			"message_id": message_id,
			"phone_number": clean_phone,
			"country_code": "+91",
			"status": "Received",
			"direction": "Incoming",
			"message_content": message_text,
			"media_url": media_url,
			"reference_doctype": reference_doctype,
			"reference_docname": reference_docname,
		})
		
		doc.insert(ignore_permissions=True)
		
		frappe.logger().info(f"Incoming message saved: {doc.name}")
		
		# Commit first so data is available for frontend to fetch
		frappe.db.commit()
		
		# DEBUG: Log site name and publish details
		frappe.logger().info(f"[WEBHOOK DEBUG] frappe.local.site = {frappe.local.site}")
		frappe.logger().info(f"[WEBHOOK DEBUG] Publishing realtime event: reference_doctype={reference_doctype}, reference_name={reference_docname}")
		
		# Publish directly (not after_commit) since data is already committed
		frappe.publish_realtime(
			"whatsapp_message",
			{
				"reference_doctype": reference_doctype,
				"reference_name": reference_docname,
			},
		)
		
		frappe.logger().info("[WEBHOOK DEBUG] publish_realtime called successfully")
		
	except Exception as e:
		frappe.log_error(
			title="Error handling incoming message",
			message=f"Error: {str(e)}\nWebhook data: {json.dumps(webhook_data, indent=2)}"
		)


def handle_status_update(webhook_data):
	"""
	Handle message status updates (sent, delivered, read).
	
	Webhook format:
	{
		"type": "message_status_update",
		"data": {
			"message_id": "message-id",
			"status": "delivered",
			"delivered_at_utc": "2022-06-03T05:58:00.000000"
		}
	}
	"""
	try:
		data = webhook_data.get("data") or webhook_data
		# Interakt payload uses 'id' for the message id in status updates
		message_id = data.get("id") or data.get("message_id")
		status = data.get("status", "").lower()
		
		if not message_id:
			frappe.logger().error(f"No message_id in status update: {json.dumps(webhook_data)}")
			return
		
		# Find message by message_id
		message_name = frappe.db.get_value(
			"CRM WhatsApp Message",
			{"message_id": message_id},
			"name"
		)
		
		if not message_name:
			frappe.logger().info(f"Message not found: {message_id}")
			return
		
		# Update status
		doc = frappe.get_doc("CRM WhatsApp Message", message_name)
		
		# Map Interakt status to our status
		status_map = {
			"sent": "Sent",
			"delivered": "Delivered",
			"read": "Read",
			"failed": "Failed"
		}
		
		new_status = status_map.get(status, "Sent")
		doc.status = new_status
		
		# Update timestamps
		if status == "delivered" and data.get("delivered_at_utc"):
			doc.delivered_at = data.get("delivered_at_utc")
		elif status == "read" and data.get("read_at_utc"):
			doc.read_at = data.get("read_at_utc")
		
		doc.save(ignore_permissions=True)
		
		# Commit first so data is available for frontend to fetch
		frappe.db.commit()
		
		# Publish directly (not after_commit) since data is already committed
		frappe.publish_realtime(
			"whatsapp_message",
			{
				"reference_doctype": doc.reference_doctype,
				"reference_name": doc.reference_docname,
			},
		)
		
		frappe.logger().info(f"Status updated: {message_name} -> {new_status}")
		
	except Exception as e:
		frappe.log_error(
			title="Error handling status update",
			message=f"Error: {str(e)}\nWebhook data: {json.dumps(webhook_data, indent=2)}"
		)


def find_document_by_phone(phone_number):
	"""
	Find Lead/Deal/Contact by phone number.
	Handles inconsistent phone number formats (spaces, dashes, country codes).
	Returns: (doctype, docname) or (None, None)
	"""
	# Strip all non-digit characters from input
	clean_digits = "".join(filter(str.isdigit, str(phone_number)))
	
	if not clean_digits:
		return (None, None)
	
	# Get default country code from settings
	settings = frappe.get_single("CRM Interakt Settings")
	default_country_code = settings.default_country_code or "+91"
	country_code_digits = default_country_code.lstrip("+")
	
	# Strip country code from the start if present
	if clean_digits.startswith(country_code_digits):
		local_number = clean_digits[len(country_code_digits):]
	else:
		local_number = clean_digits
	
	frappe.logger().info(f"Phone matching: input={phone_number}, clean_digits={clean_digits}, local_number={local_number}")
	
	# Build SQL that strips spaces/dashes from stored phone numbers and matches
	# We use REPLACE to strip common formatting characters from the DB value
	# Then check if the cleaned DB value ends with our local number
	strip_sql = """
		REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
			{field}, ' ', ''), '-', ''), '(', ''), ')', ''), '+', '')
	"""
	
	# Search in CRM Lead (mobile_no and phone fields)
	for field in ["mobile_no", "phone"]:
		stripped = strip_sql.format(field=field)
		result = frappe.db.sql("""
			SELECT name FROM `tabCRM Lead`
			WHERE {stripped} LIKE %s
			   OR {stripped} LIKE %s
			   OR {stripped} = %s
			ORDER BY creation DESC
			LIMIT 1
		""".format(stripped=stripped), (
			f"%{local_number}",         # ends with local number
			f"%{clean_digits}",          # ends with full number including country code  
			local_number,                # exact match after stripping
		), as_dict=True)
		
		if result:
			frappe.logger().info(f"Phone matched CRM Lead: {result[0].name} via {field}")
			return ("CRM Lead", result[0].name)
	
	# Search in CRM Deal
	for field in ["mobile_no"]:
		stripped = strip_sql.format(field=field)
		result = frappe.db.sql("""
			SELECT name FROM `tabCRM Deal`
			WHERE {stripped} LIKE %s
			   OR {stripped} LIKE %s
			   OR {stripped} = %s
			ORDER BY creation DESC
			LIMIT 1
		""".format(stripped=stripped), (
			f"%{local_number}",
			f"%{clean_digits}",
			local_number,
		), as_dict=True)
		
		if result:
			frappe.logger().info(f"Phone matched CRM Deal: {result[0].name} via {field}")
			return ("CRM Deal", result[0].name)
	
	# Search in Contact
	for field in ["mobile_no", "phone"]:
		stripped = strip_sql.format(field=field)
		result = frappe.db.sql("""
			SELECT name FROM `tabContact`
			WHERE {stripped} LIKE %s
			   OR {stripped} LIKE %s
			   OR {stripped} = %s
			ORDER BY creation DESC
			LIMIT 1
		""".format(stripped=stripped), (
			f"%{local_number}",
			f"%{clean_digits}",
			local_number,
		), as_dict=True)
		
		if result:
			frappe.logger().info(f"Phone matched Contact: {result[0].name} via {field}")
			return ("Contact", result[0].name)
	
	return (None, None)

