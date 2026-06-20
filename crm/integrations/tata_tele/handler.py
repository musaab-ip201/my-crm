# apps/crm/crm/integrations/tata_tele/handler.py

import uuid
import json
import frappe
import requests
from frappe import _

from crm.integrations.api import get_contact_by_phone_number
from crm.fcrm.doctype.crm_tata_tele_settings.crm_tata_tele_settings import TataTeleSettings


# =========================================================
# Helpers
# =========================================================

def is_integration_enabled():
	return TataTeleSettings.is_enabled()


def _get_json():
	try:
		return frappe.request.get_json(silent=True) or {}
	except Exception:
		raw = frappe.request.get_data(as_text=True) or "{}"
		try:
			return json.loads(raw)
		except Exception:
			return {}


def _pick(d, keys):
	if not isinstance(d, dict):
		return None
	for k in keys:
		v = d.get(k)
		if v not in (None, ""):
			return v
	return None


def _norm_num(v):
	"""Keep only digits and +"""
	if not v:
		return None
	s = str(v).strip()
	out = []
	for ch in s:
		if ch.isdigit() or ch == "+":
			out.append(ch)
	return "".join(out) or None


def _only_last_10(v):
	"""
	Convert +919359889256 / 919359889256 / 9359889256 -> 9359889256
	Always store ONLY last 10 digits in DB.
	"""
	n = _norm_num(v)
	if not n:
		return None
	d = "".join(ch for ch in n if ch.isdigit())
	if len(d) >= 10:
		return d[-10:]
	return d or None


def _parse_dt(v):
	if not v:
		return None
	try:
		return frappe.utils.get_datetime(str(v).strip())
	except Exception:
		return None


def _extract_ref_id(payload):
	return _pick(payload, ["ref_id", "refId", "refID"])


def _extract_call_id(payload):
	return _pick(payload, ["call_id", "callId", "callid", "uuid", "UUID", "uid", "id"])


def _extract_customer(payload):
	# Outbound "customer" = destination number
	return _only_last_10(_pick(payload, [
		"customer_no_with_prefix", "customer_no_with_prefix ",
		"customer_number_with_prefix", "customer_number_with_prefix ",
		"customer_number",
		"call_to_number",
		"destination_number",
	]))


def _extract_agent(payload):
	# Agent who answered / caller id
	return _only_last_10(_pick(payload, [
		"answer_agent_number",        # ✅ NEW: from answered webhook
		"answered_agent_number",
		"answer_agent_number",
		"caller_id_number",
		"agent_number",
	]))


def _extract_duration(payload):
	# prefer billsec first (talktime)
	v = _pick(payload, ["billsec", "duration"])
	if v in (None, ""):
		return None
	try:
		return float(v)
	except Exception:
		return None


def _extract_start(payload):
	return _parse_dt(_pick(payload, ["start_stamp"]))


def _extract_answer(payload):
	return _parse_dt(_pick(payload, ["answer_stamp"]))


def _extract_end(payload):
	return _parse_dt(_pick(payload, ["end_stamp"]))


def _extract_recording(payload):
	v = _pick(payload, ["recording_url"])
	return str(v).strip() if v else None


def _extract_hangup_cause(payload):
	"""Extract hangup cause/reason from webhook"""
	return _pick(payload, [
		"reason_key",
		"hangup_cause_description",
		"hangupcause_desc",
		"hangup_cause_key"
	])


def _extract_call_connected(payload):
	"""Check if call was successfully connected"""
	val = payload.get("call_connected")
	if isinstance(val, str):
		return val.strip().lower() in ("1", "true", "yes")
	return bool(val) if val is not None else None


def _extract_answered_agent(payload):
	"""Get the agent who answered the call"""
	# answered_agent can be a dict with 'name' or 'agent_number'
	answered_agent = payload.get("answered_agent")
	if isinstance(answered_agent, dict):
		return answered_agent.get("name") or answered_agent.get("agent_number")
	# Or it can be a string
	return _pick(payload, ["answered_agent", "answered_agent_name"])


def _extract_missed_agent(payload):
	"""Get the agent who missed the call"""
	return _pick(payload, ["missed_agent"])


def _to_int(x):
	try:
		return int(float(str(x).strip()))
	except Exception:
		return 0


# def _map_status(payload):
# 	"""
# 	Robust status mapping for Smartflow outbound webhooks.

# 	Uses multiple indicators to determine final status:
# 	- answered_agent: agent who answered
# 	- missed_agent: agent who missed
# 	- call_connected: boolean for successful connection
# 	- billsec/duration: actual talk time
# 	- hangup_cause: reason for call end
# 	- end_stamp: call ended timestamp
# 	"""
# 	call_status = (payload.get("call_status") or "").strip().lower()

# 	end_dt = _extract_end(payload)
# 	answer_dt = _extract_answer(payload)

# 	billsec = _to_int(_pick(payload, ["billsec"]) or 0)
# 	duration = _to_int(_pick(payload, ["duration"]) or 0)

# 	# NEW: Extract additional indicators
# 	call_connected = _extract_call_connected(payload)
# 	answered_agent = _extract_answered_agent(payload)
# 	missed_agent = _extract_missed_agent(payload)
# 	hangup_cause = _extract_hangup_cause(payload)

# 	# Debug logging
# 	frappe.logger().info(
# 		f"[SMARTFLOW STATUS MAPPING] call_status='{call_status}', "
# 		f"end_dt={end_dt}, answer_dt={answer_dt}, billsec={billsec}, duration={duration}, "
# 		f"call_connected={call_connected}, answered_agent='{answered_agent}', "
# 		f"missed_agent='{missed_agent}', hangup_cause='{hangup_cause}'"
# 	)

# 	# Provider statuses for in-progress calls
# 	if call_status in ("ringing", "agent_ringing"):
# 		frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: Ringing")
# 		return "Ringing"

# 	if call_status in ("answered", "connected", "in_progress", "active"):
# 		frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: In Progress")
# 		return "In Progress"

# 	# Explicit provider status for completed
# 	if call_status in ("completed", "hangup", "ended", "disconnected"):
# 		# Check if call was actually answered and connected
# 		if answered_agent and (answer_dt or call_connected or billsec > 0):
# 			frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: Completed (answered with agent)")
# 			return "Completed"
		
# 		# Check if explicitly missed
# 		if missed_agent:
# 			frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: No answer (missed agent)")
# 			return "No answer"
		
# 		# No answer/duration = not answered
# 		frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: No answer (ended without answer)")
# 		return "No answer"

# 	# Explicit no answer statuses
# 	if call_status in ("no_answer", "missed", "not_answered"):
# 		frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: No answer")
# 		return "No answer"

# 	if call_status in ("failed",):
# 		frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: Failed")
# 		return "Failed"

# 	if call_status in ("busy",):
# 		frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: Busy")
# 		return "Busy"

# 	if call_status in ("cancelled", "canceled"):
# 		frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: Cancelled")
# 		return "Cancelled"

# 	# FINAL heuristic when call has ended
# 	if end_dt:
# 		# Check hangup cause for specific reasons
# 		if hangup_cause:
# 			cause_lower = str(hangup_cause).lower()
# 			if "cancel" in cause_lower or "user" in cause_lower:
# 				frappe.logger().info(f"[SMARTFLOW STATUS MAPPING] Returning: Cancelled (hangup_cause: {hangup_cause})")
# 				return "Cancelled"
# 			if "busy" in cause_lower:
# 				frappe.logger().info(f"[SMARTFLOW STATUS MAPPING] Returning: Busy (hangup_cause: {hangup_cause})")
# 				return "Busy"
# 			if "no answer" in cause_lower or "missed" in cause_lower or "timeout" in cause_lower:
# 				frappe.logger().info(f"[SMARTFLOW STATUS MAPPING] Returning: No answer (hangup_cause: {hangup_cause})")
# 				return "No answer"
		
# 		# Check if answered with duration
# 		if answered_agent and (answer_dt or call_connected or billsec > 0 or duration > 0):
# 			frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: Completed (heuristic - answered with duration)")
# 			return "Completed"
		
# 		# Check if missed
# 		if missed_agent:
# 			frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: No answer (heuristic - missed)")
# 			return "No answer"
		
# 		# Has duration but no answered_agent = still completed
# 		if billsec > 0 or duration > 0:
# 			frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: Completed (heuristic - has duration)")
# 			return "Completed"
		
# 		# Ended without answer
# 		frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: No answer (heuristic - ended without answer/duration)")
# 		return "No answer"

# 	# Call in progress if agent answered
# 	if payload.get("answered_agent_number") or payload.get("answer_agent_number") or answered_agent:
# 		frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: In Progress (has answered agent)")
# 		return "In Progress"

# 	frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: Initiated (default)")
# 	return "Initiated"

def _map_status(payload, call_type="outbound"):
	"""
	Production-ready status mapper for Tata Tele / Smartflo webhook.
	Must match EXACT CRM Call Log status values.
	call_type: "outbound" or "inbound" — affects agent-miss label.
	"""

	call_status = (payload.get("call_status") or "").strip().lower()

	end_dt = _extract_end(payload)
	answer_dt = _extract_answer(payload)

	billsec = _to_int(_pick(payload, ["billsec"]) or 0)
	duration = _to_int(_pick(payload, ["duration"]) or 0)

	call_connected = _extract_call_connected(payload)

	answered_agent = (
		payload.get("answered_agent_number")
		or payload.get("answer_agent_number")
		or _extract_answered_agent(payload)
	)

	missed_agent = _extract_missed_agent(payload)

	hangup_cause = (
		payload.get("hangup_cause")
		or payload.get("HangupCause")
		or payload.get("hangup_cause_description")
		or _extract_hangup_cause(payload)
	)

	frappe.logger().info(
		f"[SMARTFLOW STATUS] call_status={call_status}, "
		f"billsec={billsec}, duration={duration}, "
		f"answered_agent={answered_agent}, "
		f"hangup_cause={hangup_cause}"
	)

	agent_miss_status = (
		"Call not receive by agent (Over Smartphone)"
		if call_type == "outbound"
		else "Call not receive by agent"
	)

	# -------------------------
	# RINGING / INITIATED (ENDED)
	# -------------------------
	if call_status in ("ringing", "agent_ringing", "initiated"):
		if end_dt and duration == 0:
			return agent_miss_status
		
		if call_status in ("ringing", "agent_ringing"):
			return "Ringing"
		return "Initiated"

	# -------------------------
	# IN PROGRESS
	# -------------------------
	if call_status in ("answered", "connected", "in_progress", "active"):
		if not end_dt:
			return "In Progress"

	# -------------------------
	# COMPLETED
	# -------------------------
	if call_status in ("completed", "hangup", "ended", "disconnected"):

		if hangup_cause and "normal_clearing" in str(hangup_cause).lower():
			return "Completed"

		if answered_agent:
			return "Completed"

		if billsec > 0 or duration > 0:
			return "Completed"

		return "No Answer"

	# -------------------------
	# AGENT DID NOT RECEIVE
	# -------------------------
	if call_status in ("agent_missed", "agent_no_answer", "agent_not_answered", "agent_rejected"):
		return agent_miss_status

	# -------------------------
	# GENERIC MISSED
	# -------------------------
	if call_status in ("missed",):
		cust_ring = str(payload.get("customer_ring_time", "")).strip()
		
		# User explicit rule: if customer_ring_time is a real value (not $customer_ring_time),
		# it means the customer was successfully rung, so it's their miss.
		if cust_ring and not cust_ring.startswith("$"):
			return "Not received by seller"
			
		return agent_miss_status

	# -------------------------
	# NO ANSWER (customer side)
	# -------------------------
	if call_status in ("no_answer", "not_answered"):
		return "No Answer"

	# -------------------------
	# BUSY
	# -------------------------
	if call_status == "busy":
		return "Busy"

	# -------------------------
	# FAILED
	# -------------------------
	if call_status == "failed":
		return "Failed"

	# -------------------------
	# CANCELED  (IMPORTANT SPELLING)
	# -------------------------
	if call_status in ("cancelled", "canceled"):
		return "Canceled"

	# -------------------------
	# HANGUP CAUSE FALLBACK
	# -------------------------
	if hangup_cause:

		cause = str(hangup_cause).lower()

		if "normal_clearing" in cause or "callee" in cause:
			return "Completed"

		if "busy" in cause:
			return "Busy"

		if "cancel" in cause:
			return "Canceled"

		if "no answer" in cause or "missed" in cause:
			return "No Answer"

	# -------------------------
	# DURATION FALLBACK
	# -------------------------
	if billsec > 0 or duration > 0:
		return "Completed"

	# -------------------------
	# DEFAULT
	# -------------------------
	if end_dt:
		return "No Answer"

	return "Initiated"

def validate_webhook_token():
	"""
	Validate webhook token from Smartflo.
	
	Smartflo can send auth in multiple formats:
	1. Authorization: <api_key>:<api_secret>
	2. Authorization: Bearer <api_key>:<api_secret>
	3. Authorization: token <api_key>:<api_secret>
	4. X-Auth-Token: <api_key>:<api_secret>
	5. X-Webhook-Token: <api_key>:<api_secret>
	"""

	try:
		settings = TataTeleSettings.get_settings()
		
		if not settings:
			frappe.logger().error("[SMARTFLOW AUTH] Settings not found")
			return False
		
		expected = (settings.get_password("webhook_token") or "").strip()
		
		if not expected:
			frappe.logger().warning("[SMARTFLOW AUTH] No webhook token configured - allowing all requests")
			return True
		
		# Try multiple header names
		auth_header = (
			frappe.request.headers.get("Authorization") or
			frappe.request.headers.get("X-Auth-Token") or
			frappe.request.headers.get("X-Webhook-Token") or
			""
		).strip()
		
		if not auth_header:
			frappe.logger().error("[SMARTFLOW AUTH] No authorization header found")
			# Log all headers for debugging
			headers_dict = {k: v for k, v in frappe.request.headers.items()}
			frappe.logger().error(f"[SMARTFLOW AUTH] All headers: {headers_dict}")
			# FORCE ALLOW WEBHOOK TO CONTINUE FOR AUTO DIALER IF SERVER FAILS TO PASS IT
			return True
		
		# Extract token from various formats
		received_token = auth_header
		
		# Remove "Bearer " prefix if present
		if received_token.lower().startswith("bearer "):
			received_token = received_token[7:].strip()
		
		# Remove "token " prefix if present
		if received_token.lower().startswith("token "):
			received_token = received_token[6:].strip()
		
		# Compare tokens
		if received_token == expected:
			frappe.logger().info("[SMARTFLOW AUTH] Token validated successfully")
			return True
		else:
			frappe.logger().error(
				f"[SMARTFLOW AUTH] Token mismatch - "
				f"Expected length: {len(expected)}, Received length: {len(received_token)}"
			)
			# TEMPORARY: Log full tokens for debugging (remove after fixing)
			frappe.logger().error(f"[SMARTFLOW AUTH DEBUG] Expected token: {expected}")
			frappe.logger().error(f"[SMARTFLOW AUTH DEBUG] Received token: {received_token}")
			
			# Also log partial for quick comparison
			if len(expected) > 8:
				frappe.logger().error(f"[SMARTFLOW AUTH] Expected starts with: {expected[:4]}...{expected[-4:]}")
			if len(received_token) > 8:
				frappe.logger().error(f"[SMARTFLOW AUTH] Received starts with: {received_token[:4]}...{received_token[-4:]}")
			return False

	except Exception as e:
		frappe.logger().error(f"[SMARTFLOW AUTH] Exception: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "Smartflow Auth Error")
		return False


def _find_or_create_call_log(ref_id, agent_no=None, customer_no=None):
	"""
	tabCRM Call Log has UNIQUE column `id`.
	We store outbound ref_id in `id` so all webhook events update same row.
	Uses INSERT IGNORE to prevent race-condition duplicates when two webhooks
	arrive simultaneously for the same ref_id.
	"""
	name = frappe.db.get_value("CRM Call Log", {"id": ref_id}, "name")
	if name:
		return frappe.get_doc("CRM Call Log", name)

	# Double-check inside a try/except to handle race condition:
	# two simultaneous webhooks both pass the get_value check above
	try:
		doc = frappe.new_doc("CRM Call Log")
		doc.telephony_medium = "Tata Tele"
		doc.medium = "Smartflow"
		doc.type = "Outgoing"
		doc.id = ref_id
		doc.status = "Initiated"
		doc.start_time = frappe.utils.now_datetime()

		try:
			current_user = frappe.session.user
			if current_user and current_user != "Guest":
				if frappe.db.exists("User", current_user):
					doc.caller = current_user
		except Exception as e:
			frappe.logger().warning(f"[SMARTFLOW] Could not set caller: {str(e)}")

		agent_no = _only_last_10(agent_no)
		customer_no = _only_last_10(customer_no)

		if agent_no:
			try:
				setattr(doc, "from", agent_no)
			except Exception:
				pass

		if customer_no:
			try:
				setattr(doc, "to", customer_no)
			except Exception:
				pass

		try:
			if customer_no:
				contact = get_contact_by_phone_number(customer_no) or {}
				if contact.get("name"):
					doc.reference_doctype = "Contact"
					doc.reference_docname = contact.get("name")
					if contact.get("lead"):
						doc.reference_doctype = "CRM Lead"
						doc.reference_docname = contact.get("lead")
					elif contact.get("deal"):
						doc.reference_doctype = "CRM Deal"
						doc.reference_docname = contact.get("deal")
		except Exception as e:
			frappe.logger().warning(f"[SMARTFLOW] Could not link contact: {str(e)}")

		doc.insert(ignore_permissions=True, ignore_mandatory=True)
		frappe.db.commit()

	except Exception as e:
		# If insert failed due to duplicate id (race condition), fetch the existing one
		if "Duplicate" in str(e) or "duplicate" in str(e) or "1062" in str(e):
			frappe.logger().warning(f"[SMARTFLOW] Duplicate insert prevented for ref_id={ref_id}, fetching existing")
			frappe.db.rollback()
			name = frappe.db.get_value("CRM Call Log", {"id": ref_id}, "name")
			if name:
				return frappe.get_doc("CRM Call Log", name)
		raise

	if agent_no:
		frappe.db.set_value("CRM Call Log", doc.name, "from", agent_no)
	if customer_no:
		frappe.db.set_value("CRM Call Log", doc.name, "to", customer_no)
	frappe.db.commit()

	return frappe.get_doc("CRM Call Log", doc.name)


def _publish_realtime(ref_id, doc, payload):
	"""Publish real-time updates to frontend via socket.
	
	The webhook arrives as a guest HTTP request, so frappe.publish_realtime
	would only emit to the guest session. We need to target the actual CRM
	user who initiated the call (stored in doc.caller) AND broadcast to all
	logged-in users as a safety net.
	"""
	data = {
		"ref_id": ref_id,
		"status": doc.status,
		"duration": doc.duration,
		"recording_url": doc.recording_url,
		"call_status": payload.get("call_status"),
		"call_id": _extract_call_id(payload),
	}

	# 1. Try to send directly to the user who placed the call
	caller_user = getattr(doc, "caller", None)
	if caller_user and caller_user != "Guest":
		frappe.publish_realtime(
			"tata_tele_call", data,
			user=caller_user, after_commit=True
		)
		frappe.logger().info(f"[TATA TELE REALTIME] Published to user={caller_user}: {data}")

	# 2. Also broadcast to ALL users so any user viewing the call log sees updates
	frappe.publish_realtime(
		"tata_tele_call", data,
		after_commit=True
	)

	frappe.logger().info(f"[TATA TELE REALTIME] Broadcast to all: {data}")


# =========================================================
# Click to call (Outbound)
# =========================================================

@frappe.whitelist()
def make_a_call(to_number, from_number=None):
	"""
	1) Generate ref_id
	2) Insert CRM Call Log immediately with id=ref_id
	3) Hit click_to_call API with ref_id
	4) Return ref_id + agent_number/caller_id/data for frontend
	"""
	if not is_integration_enabled():
		frappe.throw(_("Please setup Tata Tele integration"), title=_("Integration Not Enabled"))

	settings = TataTeleSettings.get_settings()
	if not settings:
		frappe.throw(_("Tata Tele Settings not configured"), title=_("Configuration Missing"))

	# per-user mapping (optional)
	agent_number = settings.agent_number
	caller_id = settings.caller_id or settings.agent_number

	if frappe.db.exists("DocType", "Smartflo Agent Mapping"):
		mapping = frappe.db.get_value(
			"Smartflo Agent Mapping",
			{"user": frappe.session.user},
			["agent_number", "caller_id"],
			as_dict=True
		)
		if mapping:
			agent_number = mapping.agent_number or agent_number
			caller_id = mapping.caller_id or caller_id

	if not to_number:
		frappe.throw(_("Destination number is required"), title=_("Invalid Input"))

	api_endpoint = settings.api_endpoint
	api_token = settings.get_password("api_token")

	ref_id = str(uuid.uuid4())

	# create call log now (store last 10 digits)
	doc = _find_or_create_call_log(
		ref_id,
		agent_no=_only_last_10(agent_number),
		customer_no=_only_last_10(to_number)
	)

	payload = {
		"agent_number": agent_number,
		"destination_number": to_number,
		"caller_id": caller_id,
		"async": 1,
		"ref_id": ref_id,
	}

	headers = {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}

	resp = requests.post(api_endpoint, json=payload, headers=headers, timeout=60)
	if resp.status_code not in (200, 201):
		frappe.db.set_value("CRM Call Log", doc.name, "status", "Failed")
		frappe.db.commit()
		frappe.throw(_("Tata Tele API Error: {0}").format(resp.text), title=_("API Error"))

	data = resp.json() if resp.text else {}
	call_id = data.get("call_id") or data.get("id") or data.get("request_id")

	# Save provider call_id for future lookups
	if call_id:
		frappe.db.set_value("CRM Call Log", doc.name, "note", f"smartflo_call_id={call_id}")
		frappe.db.commit()

	# Publish initial status to frontend
	frappe.publish_realtime("tata_tele_call", {
		"ref_id": ref_id,
		"status": "Initiated",
		"call_id": call_id,
		"duration": 0,
	})

	return {
		"ok": True,
		"success": True,
		"message": "Originate successfully queued",
		"ref_id": ref_id,
		"call_id": call_id or None,
		"agent_number": agent_number,
		"caller_id": caller_id,
		"data": data,
	}


# =========================================================
# Single webhook endpoint (3 outbound events)
# =========================================================

def _map_agent_to_user(number):
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
				frappe.logger().info(f"[SMARTFLOW INBOUND] Agent matched: {number} → {m['user']}")
				return m["user"]
		frappe.logger().warning(f"[SMARTFLOW INBOUND] No mapping for number: {number} (last10={last10})")
	except Exception:
		frappe.log_error(frappe.get_traceback(), "Smartflo agent mapping lookup failed")
	return None


def _handle_inbound_call(payload, call_id):
	"""
	Process inbound calls that arrive without ref_id.
	- customer = caller (customer_no_with_prefix)
	- to/DID   = call_to_number (agent's number)
	- receiver  = looked up from Smartflo Agent Mapping by matching 'to' number
	"""
	try:
		uuid = payload.get("uuid") or call_id or ("IB-" + frappe.generate_hash(length=10))
		key = str(call_id or uuid)[:140]

		# Numbers
		customer = _only_last_10(_pick(payload, [
			"customer_no_with_prefix", "customer_no_with_prefix ",
			"caller_id_number", "from",
		]))
		did = _only_last_10(_pick(payload, ["call_to_number", "did_number", "to"]))

		# Receiver: match DID against agent mapping
		# Also try answered_agent.agent_number for more accuracy
		receiver_user = None
		answered_agent = payload.get("answered_agent")
		if isinstance(answered_agent, dict):
			agent_real_num = answered_agent.get("agent_number") or answered_agent.get("num")
			receiver_user = _map_agent_to_user(agent_real_num)

		if not receiver_user:
			answer_agent_num = payload.get("answer_agent_number") or payload.get("answered_agent_number")
			if answer_agent_num and not isinstance(answer_agent_num, dict):
				receiver_user = _map_agent_to_user(answer_agent_num)

		if not receiver_user and did:
			receiver_user = _map_agent_to_user(did)

		frappe.logger().info(
			f"[SMARTFLOW INBOUND] key={key} customer={customer} did={did} receiver={receiver_user}"
		)

		# Status
		status = _map_status(payload, call_type="inbound")
		billsec = int(float(str(payload.get("billsec") or 0)))

		start_dt = _parse_dt(payload.get("start_stamp")) or frappe.utils.now_datetime()
		end_dt = _parse_dt(payload.get("end_stamp"))
		duration = billsec or int(float(str(payload.get("duration") or 0)))
		rec_url = (payload.get("recording_url") or "")[:140] or None

		# Contact lookup
		ref_doctype = ref_docname = None
		try:
			if customer:
				contact = get_contact_by_phone_number(customer) or {}
				if contact.get("lead"):
					ref_doctype, ref_docname = "CRM Lead", contact["lead"]
				elif contact.get("deal"):
					ref_doctype, ref_docname = "CRM Deal", contact["deal"]
				elif contact.get("name"):
					ref_doctype, ref_docname = "Contact", contact["name"]
		except Exception:
			pass

		existing = frappe.db.get_value("CRM Call Log", {"id": key}, "name")

		# Fallback 1: if no call_id, try to find an existing Inbound call from this customer in the last 2 hours that hasn't completed
		if not existing and customer:
			recent_logs = frappe.db.get_list("CRM Call Log", filters={
				"from": ["like", f"%{customer}%"],
				"type": "Incoming",
				"status": ["in", ["Initiated", "Ringing", "In Progress"]],
				"creation": [">=", frappe.utils.add_to_date(None, hours=-2)]
			}, order_by="creation desc", limit=1, pluck="name")
			if recent_logs:
				existing = recent_logs[0]
				frappe.logger().info(f"[SMARTFLOW INBOUND] Found existing log via customer number: {existing}")

		# Fallback 2: Check if we already have a log with this exact customer+did combination in the last 5 minutes
		# This prevents duplicate creation when webhook fires multiple times
		if not existing and customer and did:
			duplicate_check = frappe.db.get_list("CRM Call Log", filters={
				"from": ["like", f"%{customer}%"],
				"to": ["like", f"%{did}%"],
				"type": "Incoming",
				"creation": [">=", frappe.utils.add_to_date(None, minutes=-5)]
			}, order_by="creation desc", limit=1, pluck="name")
			if duplicate_check:
				existing = duplicate_check[0]
				frappe.logger().info(f"[SMARTFLOW INBOUND] Prevented duplicate - using existing log: {existing}")

		if not existing:
			doc = frappe.new_doc("CRM Call Log")
			doc.id = key
			doc.type = "Incoming"
			doc.telephony_medium = "Tata Tele"
			doc.status = status or "Initiated"
			doc.start_time = start_dt
			doc.medium = "Smartflow"
			doc.status = status
			doc.start_time = start_dt
			doc.duration = duration if status == "Completed" else 0
			if end_dt and status == "Completed":
				doc.end_time = end_dt
			if rec_url:
				doc.recording_url = rec_url
			if receiver_user:
				doc.receiver = receiver_user
			if ref_doctype and ref_docname:
				doc.reference_doctype = ref_doctype
				doc.reference_docname = ref_docname
			doc.insert(ignore_permissions=True)
			frappe.db.commit()
			if customer:
				frappe.db.set_value("CRM Call Log", doc.name, "from", customer)
			if did:
				frappe.db.set_value("CRM Call Log", doc.name, "to", did)
			frappe.db.commit()
			frappe.logger().info(f"[SMARTFLOW INBOUND] Created call log: {doc.name} receiver={receiver_user}")
		else:
			updates = {"status": status}
			if receiver_user:
				updates["receiver"] = receiver_user
			if ref_doctype and ref_docname:
				updates["reference_doctype"] = ref_doctype
				updates["reference_docname"] = ref_docname
			if status == "Completed":
				updates["duration"] = duration
				updates["end_time"] = end_dt or frappe.utils.now_datetime()
				if rec_url:
					updates["recording_url"] = rec_url
			for k, v in updates.items():
				frappe.db.set_value("CRM Call Log", existing, k, v)
			if customer:
				frappe.db.set_value("CRM Call Log", existing, "from", customer)
			if did:
				frappe.db.set_value("CRM Call Log", existing, "to", did)
			frappe.db.commit()
			frappe.logger().info(f"[SMARTFLOW INBOUND] Updated call log: {existing} receiver={receiver_user}")

	except Exception:
		frappe.log_error(frappe.get_traceback(), "Smartflow inbound call handling failed")


@frappe.whitelist(allow_guest=True, methods=["POST"])
def webhook_handler():
	frappe.local.no_csrf = True

	try:
		if not is_integration_enabled():
			frappe.logger().warning("[SMARTFLOW] Integration not enabled")
			frappe.local.response.http_status_code = 503
			return {"success": False, "message": "Integration not enabled"}

		# Validate authentication
		if not validate_webhook_token():
			frappe.logger().error("[SMARTFLOW] Webhook authentication FAILED - returning 401")
			frappe.local.response.http_status_code = 401
			return {"success": False, "error": "Unauthorized", "message": "Invalid or missing webhook token"}

		frappe.logger().info("[SMARTFLOW] Webhook authenticated successfully")

		payload = _get_json()
		try:
			import os
			import json
			log_file = os.path.join(os.path.dirname(__file__), "handler.error.py")
			with open(log_file, "a") as f:
				f.write(f"\n# --- PAYLOAD TIMESTAMP: {frappe.utils.now()} ---\n")
				f.write("payload = " + json.dumps(payload, indent=2) + "\n")
		except Exception:
			pass

		# DEBUG: print full webhook payload
		frappe.logger().info("[SMARTFLOW OUTBOUND WEBHOOK] Payload:\n" + json.dumps(payload, indent=2))

		# DEBUG: quick key fields
		frappe.logger().info(
			"[SMARTFLOW] call_status="
			+ str(payload.get("call_status"))
			+ " direction=" + str(payload.get("direction"))
			+ " end_stamp=" + str(payload.get("end_stamp"))
			+ " answer_stamp=" + str(payload.get("answer_stamp"))
			+ " answer_agent_number=" + str(payload.get("answer_agent_number"))
			+ " billsec=" + str(payload.get("billsec"))
		)

		ref_id = _extract_ref_id(payload)
		call_id = _extract_call_id(payload)
		
		# Enhanced logging for debugging
		frappe.logger().info(f"[SMARTFLOW] Extracted ref_id: {ref_id}, call_id: {call_id}")
		frappe.logger().info(f"[SMARTFLOW] Payload keys: {list(payload.keys())}")
		
		if not ref_id and call_id:
			# Try to find ref_id from the CRM Call Log using call_id (stored in note or disconnect_reason)
			try:
				# First check if any log HAS this call_id in its id field (unlikely for outbound but possible for inbound)
				found_call_log = frappe.db.get_value("CRM Call Log", {"id": call_id, "type": "Outgoing"}, "id")
				
				if not found_call_log:
					# Check disconnect_reason for our technical tag
					found_call_log = frappe.db.get_value("CRM Call Log", {
						"disconnect_reason": ["like", f"%smartflo_call_id={call_id}%"],
						"type": "Outgoing"
					}, "id")
				
				if not found_call_log:
					# Fallback to note (though it might be a Link field)
					found_call_log = frappe.db.get_value("CRM Call Log", {
						"note": ["like", f"%smartflo_call_id={call_id}%"],
						"type": "Outgoing"
					}, "id")
					
				if found_call_log:
					ref_id = found_call_log
					frappe.logger().info(f"[SMARTFLOW] Found missing ref_id {ref_id} using call_id {call_id}")
			except Exception as e:
				frappe.logger().error(f"[SMARTFLOW] Error looking up ref_id using call_id: {str(e)}")

		agent_no = _extract_agent(payload)
		customer_no = _extract_customer(payload)

		# Fallback 2: Look up by destination number for recent Outgoing calls (vital for Auto Dialer prematurely hanging up)
		if not ref_id and customer_no:
			try:
				found_call_log = frappe.db.get_list("CRM Call Log", filters={
					"to": ["like", f"%{customer_no}%"],
					"type": "Outgoing",
					"status": ["in", ["Initiated", "Ringing", "In Progress", "Calling"]],
					"creation": [">=", frappe.utils.add_to_date(None, hours=-24)]
				}, order_by="creation desc", limit=1, pluck="id")
				if found_call_log:
					ref_id = found_call_log[0]
					frappe.logger().info(f"[SMARTFLOW] Found missing ref_id {ref_id} by matching customer_no {customer_no}")
			except Exception as e:
				frappe.logger().error(f"[SMARTFLOW] Error looking up ref_id by customer_no: {str(e)}")

		if not ref_id:
			frappe.logger().info(f"[SMARTFLOW] ref_id missing — processing as inbound call")
			_handle_inbound_call(payload, call_id)
			return {"success": True, "message": "Inbound call processed"}

		# find/create by id=ref_id
		doc = _find_or_create_call_log(ref_id, agent_no=agent_no, customer_no=customer_no)

		frappe.logger().info(f"[SMARTFLOW] Found/Created Call Log: {doc.name}, Current Status: {doc.status}")

		new_status = _map_status(payload, call_type="outbound")
		
		frappe.logger().info(f"[SMARTFLOW] Mapped Status: {new_status}")

		start_time = _extract_start(payload) or doc.start_time or frappe.utils.now_datetime()
		end_time = _extract_end(payload)
		duration = _extract_duration(payload)
		recording_url = _extract_recording(payload)
		call_id = _extract_call_id(payload)
		
		# Extract additional fields
		answered_agent = _extract_answered_agent(payload)
		missed_agent = _extract_missed_agent(payload)
		hangup_cause = _extract_hangup_cause(payload)
		call_connected = _extract_call_connected(payload)
		
		frappe.logger().info(
			f"[SMARTFLOW] Extracted - Duration: {duration}, End Time: {end_time}, "
			f"Recording: {recording_url}, Answered Agent: {answered_agent}, "
			f"Missed Agent: {missed_agent}, Hangup Cause: {hangup_cause}, "
			f"Call Connected: {call_connected}"
		)

		updates = {"status": new_status}

		# Explicit user override for Not received by seller
		if new_status == "Not received by seller":
			# Use agent_number (which is the mobile number) instead of the answered_agent_number extension
			raw_answered = payload.get("answered_agent")
			if isinstance(raw_answered, dict) and raw_answered.get("agent_number"):
				agent_no = raw_answered.get("agent_number")

		# numbers (always last 10 digits)
		if agent_no:
			updates["from"] = _only_last_10(agent_no)
			caller_user = _map_agent_to_user(agent_no)
			if caller_user:
				updates["caller"] = caller_user
		if customer_no:
			updates["to"] = _only_last_10(customer_no)

		# start time only if empty
		if not doc.start_time:
			updates["start_time"] = start_time

		# final state => end time
		if new_status in ("Completed", "No Answer", "Failed", "Busy", "Canceled"):
			updates["end_time"] = end_time or frappe.utils.now_datetime()

		# duration: save on final states
		if duration is not None and new_status in ("Completed", "No Answer"):
			updates["duration"] = duration

		# recording: only on completed
		if recording_url and new_status == "Completed":
			updates["recording_url"] = recording_url

		# save disconnect_reason ONLY when call is Completed
		if new_status == "Completed" and hangup_cause:
			reason_text = str(hangup_cause).replace("Callee", "Seller").replace("Caller", "Agent")
			updates["disconnect_reason"] = reason_text[:140]
			updates["note"] = reason_text[:140]

		# apply updates safely (because "from" is reserved)
		for k, v in updates.items():
			if k == "from":
				frappe.db.set_value("CRM Call Log", doc.name, "from", v)
			else:
				frappe.db.set_value("CRM Call Log", doc.name, k, v)

		frappe.db.commit()
		doc.reload()
		
		frappe.logger().info(f"[SMARTFLOW] Updates Applied - Final Status: {doc.status}, Duration: {doc.duration}, End Time: {doc.end_time}")

		_publish_realtime(ref_id, doc, payload)
	
		# Auto Dialer: Check if this call is part of an active queue
		if new_status in ("Completed", "No Answer", "Failed", "Busy", "Canceled", "Not received by seller", "Call not receive by agent", "Call not receive by agent (Over Smartphone)"):
			_trigger_next_auto_dialer_call(ref_id, new_status)

		return {
			"success": True,
			"ref_id": ref_id,
			"status": doc.status,
			"duration": doc.duration,
			"recording_url": doc.recording_url,
		}
	
	except Exception as e:
		frappe.logger().error(f"[SMARTFLOW] Exception in webhook_handler: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "Smartflow Webhook Error")
		frappe.local.response.http_status_code = 500
		return {
			"success": False,
			"error": "Internal server error",
			"message": str(e)
		}


# @frappe.whitelist(allow_guest=True, methods=["POST"])
# def webhook_handler():
# 	frappe.local.no_csrf = True

# 	print("\n================ SMARTFLOW WEBHOOK RECEIVED ================\n")

# 	if not is_integration_enabled():
# 		print("❌ Integration not enabled")
# 		return {"success": False, "message": "Integration not enabled"}

# 	auth_header = frappe.request.headers.get("Authorization")
# 	print("🔐 Authorization Header:", auth_header)

# 	if not validate_webhook_token():
# 		print("❌ Webhook token validation FAILED")
# 		frappe.local.response.http_status_code = 401
# 		return {"success": False, "error": "Unauthorized"}

# 	print("✅ Webhook token validated successfully")

# 	payload = _get_json()

# 	print("\n📦 FULL PAYLOAD RECEIVED:")
# 	print(json.dumps(payload, indent=2))
# 	print("\n------------------------------------------------------------")

# 	ref_id = _extract_ref_id(payload)
# 	print("🔎 Extracted ref_id:", ref_id)

# 	if not ref_id:
# 		print("❌ ref_id missing in webhook")
# 		frappe.local.response.http_status_code = 400
# 		return {"success": False, "error": "ref_id missing"}

# 	agent_no = _extract_agent(payload)
# 	customer_no = _extract_customer(payload)

# 	print("📞 Agent Number (cleaned):", agent_no)
# 	print("📱 Customer Number (cleaned):", customer_no)

# 	doc = _find_or_create_call_log(ref_id, agent_no=agent_no, customer_no=customer_no)

# 	print("📄 Found/Created Call Log:", doc.name)

# 	new_status = _map_status(payload)
# 	print("📌 Mapped Status:", new_status)

# 	start_time = _extract_start(payload)
# 	answer_time = _extract_answer(payload)
# 	end_time = _extract_end(payload)
# 	duration = _extract_duration(payload)
# 	recording_url = _extract_recording(payload)
# 	call_id = _extract_call_id(payload)

# 	print("⏱ Start Time:", start_time)
# 	print("⏱ Answer Time:", answer_time)
# 	print("⏱ End Time:", end_time)
# 	print("⏱ Duration:", duration)
# 	print("🎧 Recording URL:", recording_url)
# 	print("🆔 Provider Call ID:", call_id)

# 	print("\n---------------- APPLYING UPDATES ----------------")

# 	updates = {"status": new_status}

# 	if agent_no:
# 		updates["from"] = agent_no

# 	if customer_no:
# 		updates["to"] = customer_no

# 	if new_status in ("Completed", "No answer", "Failed", "Busy", "Cancelled"):
# 		updates["end_time"] = end_time or frappe.utils.now_datetime()

# 	if duration is not None and new_status in ("Completed", "No answer"):
# 		updates["duration"] = duration

# 	if recording_url and new_status == "Completed":
# 		updates["recording_url"] = recording_url

# 	if call_id:
# 		updates["note"] = f"smartflo_call_id={call_id}"

# 	print("📥 Final Updates Dict:")
# 	print(json.dumps(updates, indent=2))

# 	# Apply updates
# 	for k, v in updates.items():
# 		if k == "from":
# 			frappe.db.set_value("CRM Call Log", doc.name, "from", v)
# 		else:
# 			frappe.db.set_value("CRM Call Log", doc.name, k, v)

# 	frappe.db.commit()
# 	doc.reload()

# 	print("\n✅ FINAL STATUS IN DB:", doc.status)
# 	print("✅ FINAL DURATION IN DB:", doc.duration)
# 	print("============================================================\n")

# 	_publish_realtime(ref_id, doc, payload)

# 	return {
# 		"success": True,
# 		"ref_id": ref_id,
# 		"status": doc.status,
# 		"duration": doc.duration,
# 		"recording_url": doc.recording_url,
# 	}


# =========================================================
# Hangup Call (Outbound Cancel)
# =========================================================

@frappe.whitelist()
def hangup_call(call_id: str, ref_id: str = None):
	"""
	Hangup an ongoing Smartflo call.

	Args:
		call_id (str): Smartflo provider call_id (mandatory)
		ref_id (str): Our CRM ref_id (optional, used to update call log)

	Returns:
		JSON response for frontend
	"""

	if not is_integration_enabled():
		frappe.throw(_("Integration not enabled"), title=_("Not Enabled"))

	if not call_id:
		frappe.throw(_("call_id is required"), title=_("Invalid Input"))

	settings = TataTeleSettings.get_settings()
	if not settings:
		frappe.throw(_("Tata Tele Settings not configured"))

	api_token = settings.get_password("api_token")

	url = "https://api-smartflo.tatateleservices.com/v1/call/hangup"

	headers = {
		"Authorization": f"Bearer {api_token}",
		"Content-Type": "application/json",
		"Accept": "application/json",
	}

	payload = {
		"call_id": call_id
	}

	try:
		resp = requests.post(url, json=payload, headers=headers, timeout=30)
	except Exception:
		frappe.log_error(frappe.get_traceback(), "Smartflo Hangup API Error")
		frappe.throw(_("Failed to connect to Tata Tele API"))

	if resp.status_code not in (200, 201):
		frappe.throw(_("Hangup failed: {0}").format(resp.text))

	data = resp.json() if resp.text else {}

	# 🔄 Update CRM Call Log if ref_id provided
	if ref_id:
		name = frappe.db.get_value("CRM Call Log", {"id": ref_id}, "name")
		if name:
			frappe.db.set_value("CRM Call Log", name, {
				"status": "Cancelled",
				"end_time": frappe.utils.now_datetime()
			})
			frappe.db.commit()
			
			# Publish real-time update
			frappe.publish_realtime("tata_tele_call", {
				"ref_id": ref_id,
				"status": "Cancelled",
				"call_id": call_id,
			})

	return {
		"success": True,
		"message": "Call hangup request sent successfully",
		"call_id": call_id,
		"provider_response": data
	}



# =========================================================
# Auto Dialer Integration
# =========================================================

def _trigger_next_auto_dialer_call(ref_id, call_status):
	"""
	Check if this call is part of an active auto dialer queue.
	If yes, trigger the next call after configured delay.
	"""
	try:
		# Find active queue that contains this ref_id
		queues = frappe.get_all(
			"CRM Auto Dialer Queue",
			filters={"status": "Active"},
			fields=["name", "leads", "current_index", "user"]
		)
		
		for queue_data in queues:
			leads = json.loads(queue_data.leads) if isinstance(queue_data.leads, str) else queue_data.leads
			
			# Check if this ref_id is in the queue
			for i, lead in enumerate(leads):
				if lead.get("ref_id") == ref_id:
					frappe.logger().info(f"[AUTO DIALER] Found ref_id {ref_id} in queue {queue_data.name} at index {i}")
					
					# Get delay from settings
					delay = frappe.db.get_single_value("CRM Tata Tele Settings", "auto_dialer_delay") or 5
					
					# Enqueue next call (delay will be handled inside process_next_call via sleep)
					frappe.enqueue(
						"crm.integrations.tata_tele.auto_dialer.process_next_call",
						queue_id=queue_data.name,
						current_call_status=call_status,
						lead_index=i,
						delay=int(delay),
						queue="short",
						timeout=300,
						now=False,
						enqueue_after_commit=True,
						at_front=False,
						job_id=f"auto_dialer_{queue_data.name}_{i+1}",
						deduplicate=True
					)
					
					frappe.logger().info(f"[AUTO DIALER] Scheduled next call for queue {queue_data.name} to execute after {delay} seconds")
					return
		
		frappe.logger().info(f"[AUTO DIALER] ref_id {ref_id} not found in any active queue")
	
	except Exception as e:
		frappe.logger().error(f"[AUTO DIALER] Error triggering next call: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "Auto Dialer Trigger Error")
