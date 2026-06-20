"""
Interakt Webhook Handler
Handles incoming webhooks from Interakt for:
- Incoming messages
- Message status updates (delivered, read)
"""

import frappe
from frappe import _
import json


def determine_content_type_from_url(media_url):
	"""
	Determine content type from media URL file extension.
	"""
	if not media_url:
		return "text"
	
	media_url_lower = media_url.lower()
	
	# Image extensions
	if any(ext in media_url_lower for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg']):
		return "image"
	
	# Document extensions
	elif any(ext in media_url_lower for ext in ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.xls', '.xlsx', '.ppt', '.pptx']):
		return "document"
	
	# Audio extensions
	elif any(ext in media_url_lower for ext in ['.mp3', '.wav', '.ogg', '.m4a', '.aac', '.flac']):
		return "audio"
	
	# Video extensions
	elif any(ext in media_url_lower for ext in ['.mp4', '.avi', '.mov', '.webm', '.mkv', '.flv', '.wmv']):
		return "video"
	
	# Default to image for unknown media types
	else:
		return "image"


@frappe.whitelist(allow_guest=True)
def handle_webhook():
	"""
	Main webhook handler for Interakt events.
	Endpoint: /api/method/crm.integrations.interakt.webhooks.handle_webhook
	"""
	try:
		# Get webhook data
		data = frappe.request.get_data(as_text=True)
		webhook_data = json.loads(data) if data else frappe.local.form_dict
		
		# Log webhook for debugging (but limit size to avoid huge logs)
		webhook_summary = {
			"type": webhook_data.get("type"),
			"message_id": webhook_data.get("data", {}).get("message", {}).get("id"),
			"phone": webhook_data.get("data", {}).get("customer", {}).get("channel_phone_number"),
		}
		frappe.logger().info(f"Interakt Webhook Received: {json.dumps(webhook_summary)}")
		
		# Get event type
		event_type = webhook_data.get("type")
		
		if event_type == "message_received":
			handle_message_received(webhook_data)
		elif event_type == "message_status_update":
			handle_status_update(webhook_data)
		else:
			frappe.logger().info(f"Unknown webhook type: {event_type}")
		
		return {"success": True, "message": "Webhook processed"}
		
	except json.JSONDecodeError as e:
		frappe.log_error(
			title="Interakt Webhook JSON Error",
			message=f"Invalid JSON in webhook: {str(e)}\nRaw data: {frappe.request.get_data(as_text=True)[:500]}..."
		)
		return {"success": False, "error": "Invalid JSON"}
	except Exception as e:
		frappe.log_error(
			title="Interakt Webhook Error",
			message=f"Error processing webhook: {str(e)}\nData: {frappe.request.get_data(as_text=True)[:500]}..."
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
		data = webhook_data.get("data", {})
		customer = data.get("customer", {})
		message = data.get("message", {})
		
		# Extract phone number
		phone_number = customer.get("channel_phone_number", "")
		if not phone_number:
			frappe.logger().error("No phone number in webhook")
			return
		
		frappe.logger().info(f"Processing message for phone: {phone_number}")
		
		# Clean phone number (remove country code for matching)
		clean_phone = phone_number.lstrip("+")
		
		# Get default country code from settings
		settings = frappe.get_single("CRM Interakt Settings")
		default_country_code = settings.default_country_code or "+91"
		country_code_digits = default_country_code.lstrip("+")
		
		if clean_phone.startswith(country_code_digits):
			clean_phone = clean_phone[len(country_code_digits):]
		
		frappe.logger().info(f"Cleaned phone number: {clean_phone}")
		
		# Find lead/deal/contact by phone number
		reference_doctype, reference_docname = find_document_by_phone(clean_phone)
		
		if not reference_doctype:
			frappe.logger().error(f"WhatsApp Webhook Matching Failed: No document found for phone: {phone_number} (cleaned: {clean_phone})")
			return
		
		frappe.logger().info(f"WhatsApp Webhook Matched: {reference_doctype} {reference_docname} for phone: {phone_number}")
		
		# Extract message details
		message_id = message.get("id")
		message_text = message.get("message", "")
		interakt_content_type = message.get("message_content_type", "Text").lower()
		media_url = message.get("media_url")
		
		frappe.logger().info(f"Message details - ID: {message_id}, Content Type: {interakt_content_type}, Media URL: {media_url}")
		
		# Map Interakt content types to frontend content types
		content_type_map = {
			"text": "text",
			"image": "image", 
			"document": "document",
			"audio": "audio",
			"video": "video",
			"sticker": "image",  # Treat stickers as images
			"location": "text"   # Treat location as text for now
		}
		content_type = content_type_map.get(interakt_content_type, "text")
		
		# If we have a media URL but content type is still text, try to determine from URL
		if media_url and content_type == "text":
			content_type = determine_content_type_from_url(media_url)
		
		frappe.logger().info(f"Final content type: {content_type}")
		
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
		
		# Insert the document first
		doc.insert(ignore_permissions=True)
		frappe.db.commit()
		
		frappe.logger().info(f"Incoming message saved: {doc.name}")
		
		# Prepare message data for real-time update
		message_data = doc.as_dict()
		message_data.update({
			"type": doc.direction,
			"message": message_text,
			"creation": frappe.utils.now(),
			"from_name": customer.get("traits", {}).get("name"),
			# Critical fields for frontend rendering
			"content_type": content_type,
			"message_type": "Text",
			"to": f"{doc.country_code}{doc.phone_number}",
			"from": f"{doc.country_code}{doc.phone_number}",
			"status": doc.status.lower(),
			"attach": media_url or "",  # Frontend expects 'attach' field
		})
		
		frappe.logger().info(f"Prepared message data for realtime: {message_data}")
		
		# Send real-time update AFTER successful database commit
		frappe.logger().info(f"Publishing Realtime Event for: {reference_doctype} {reference_docname} - Content Type: {content_type}")
		frappe.publish_realtime(
			"whatsapp_message",
			{
				"reference_doctype": reference_doctype,
				"reference_name": reference_docname,
				"message_data": message_data
			}
		)
		
		frappe.logger().info("Webhook processing completed successfully")
		
	except Exception as e:
		frappe.log_error(
			title="Error handling incoming message",
			message=f"Error: {str(e)}\nWebhook data: {json.dumps(webhook_data, indent=2)}"
		)
		frappe.logger().error(f"Error in handle_message_received: {str(e)}")
		raise


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
		data = webhook_data.get("data", {})
		message_id = data.get("message_id")
		status = data.get("status", "").lower()
		
		if not message_id:
			frappe.logger().error("No message_id in status update")
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
		
		# Save changes first
		doc.save(ignore_permissions=True)
		frappe.db.commit()
		
		frappe.logger().info(f"Status updated: {message_name} -> {new_status}")
		
		# Send real-time update AFTER successful database commit
		frappe.publish_realtime(
			"whatsapp_message",
			{
				"reference_doctype": doc.reference_doctype,
				"reference_name": doc.reference_docname,
				"message_id": message_id,
				"status": new_status.lower()
			}
		)
		
	except Exception as e:
		frappe.log_error(
			title="Error handling status update",
			message=f"Error: {str(e)}\nWebhook data: {json.dumps(webhook_data, indent=2)}"
		)


def find_document_by_phone(phone_number):
	"""
	Find Lead/Deal/Contact by phone number.
	Returns: (doctype, docname) or (None, None)
	"""
	# Get default country code from settings
	settings = frappe.get_single("CRM Interakt Settings")
	default_country_code = settings.default_country_code or "+91"
	country_code_digits = default_country_code.lstrip("+")

	# Try different phone number formats
	phone_variants = [
		phone_number,
		phone_number.lstrip("0"),
		f"0{phone_number}",
		f"{default_country_code}{phone_number}",
		f"{country_code_digits}{phone_number}",
	]
	
	frappe.logger().info(f"Searching for document with phone variants: {phone_variants}")
	
	# Search in CRM Lead
	for variant in phone_variants:
		frappe.logger().info(f"Checking CRM Lead mobile_no for: {variant}")
		lead = frappe.db.get_value(
			"CRM Lead",
			{"mobile_no": variant},
			"name"
		)
		if lead:
			frappe.logger().info(f"Found lead by mobile_no: {lead}")
			return ("CRM Lead", lead)
		
		# Also check phone field
		frappe.logger().info(f"Checking CRM Lead phone for: {variant}")
		lead = frappe.db.get_value(
			"CRM Lead",
			{"phone": variant},
			"name"
		)
		if lead:
			frappe.logger().info(f"Found lead by phone: {lead}")
			return ("CRM Lead", lead)
	
	# Search in CRM Deal
	for variant in phone_variants:
		frappe.logger().info(f"Checking CRM Deal mobile_no for: {variant}")
		deal = frappe.db.get_value(
			"CRM Deal",
			{"mobile_no": variant},
			"name"
		)
		if deal:
			frappe.logger().info(f"Found deal by mobile_no: {deal}")
			return ("CRM Deal", deal)
	
	# Search in Contact
	for variant in phone_variants:
		frappe.logger().info(f"Checking Contact mobile_no for: {variant}")
		contact = frappe.db.get_value(
			"Contact",
			{"mobile_no": variant},
			"name"
		)
		if contact:
			frappe.logger().info(f"Found contact by mobile_no: {contact}")
			return ("Contact", contact)
	
	frappe.logger().error(f"No document found for any phone variant: {phone_variants}")
	return (None, None)
