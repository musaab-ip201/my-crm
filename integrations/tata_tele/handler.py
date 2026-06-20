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
		if v not in (None, "", f"${k}"):
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
	if not v or str(v).startswith("$"):
		return None
	try:
		return frappe.utils.get_datetime(str(v).strip())
	except Exception:
		return None


def _extract_ref_id(payload):
	return _pick(payload, ["ref_id", "refId", "refID"])


def _extract_call_id(payload):
	return _pick(payload, ["call_id", "callId", "callid", "uuid"])


def _extract_customer(payload):
	# Outbound customer = destination number
	return _only_last_10(_pick(payload, [
		"customer_no_with_prefix",
		"customer_no_with_prefix ",
		"customer_number_with_prefix",
		"customer_number_with_prefix ",
		"customer_number",
		"call_to_number",
		"destination_number",
	]))


def _extract_agent(payload):
	# Primary agent / caller side number
	return _only_last_10(_pick(payload, [
		"answer_agent_number",
		"answered_agent_number",
		"caller_id_number",
		"agent_number",
	]))


def _extract_duration(payload):
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
	return str(v).strip()[:140] if v else None


def _extract_hangup_cause(payload):
	return _pick(payload, [
		"hangup_cause_description",
		"hangupcause_desc",
		"reason_key",
		"hangup_cause_key",
		"hangup_cause_code",
	])


def _extract_call_connected(payload):
	val = payload.get("call_connected")
	if isinstance(val, str):
		val = val.strip().lower()
		if val in ("1", "true", "yes"):
			return True
		if val in ("0", "false", "no"):
			return False
	return bool(val) if val is not None else None


def _extract_answered_agent(payload):
	"""
	Get the agent who answered.
	Prefer human-readable name, then number.
	"""
	answered_agent = payload.get("answered_agent")

	if isinstance(answered_agent, dict):
		return (
			answered_agent.get("name")
			or answered_agent.get("agent_number")
			or answered_agent.get("number")
		)

	return _pick(payload, [
		"answered_agent_name",
		"answered_agent_number",
		"answered_agent",
		"answer_agent_number",
	])


def _extract_missed_agent(payload):
	"""
	Get the agent who missed / did not receive / rejected.
	"""
	missed_agent = payload.get("missed_agent")

	if isinstance(missed_agent, dict):
		return (
			missed_agent.get("name")
			or missed_agent.get("agent_number")
			or missed_agent.get("number")
		)

	return _pick(payload, ["missed_agent"])


def _to_int(x):
	try:
		return int(float(str(x).strip()))
	except Exception:
		return 0


def _safe_text(v, max_len=140):
	if v is None:
		return None
	return str(v).strip()[:max_len]


def _build_note(call_id=None, hangup_cause=None, answered_agent=None, missed_agent=None, status=None):
	parts = []

	if call_id:
		parts.append(f"call_id={_safe_text(call_id, 30)}")

	if answered_agent:
		parts.append(f"answered={_safe_text(answered_agent, 25)}")

	if missed_agent:
		parts.append(f"missed={_safe_text(missed_agent, 25)}")

	if hangup_cause:
		parts.append(f"reason={_safe_text(hangup_cause, 35)}")

	if answered_agent and missed_agent:
		parts.append("routed_to_other_agent")

	if status == "Call not receive by agent" and not missed_agent:
		parts.append("agent_not_received_or_cut")

	note = ", ".join(parts)
	return note[:140] if note else None




def _map_status(payload, call_type="outbound"):
	"""
	Status mapping rules:

	1. If another agent answered -> Completed / In Progress
	2. If agent missed / rejected / cut before answer -> Call not receive by agent (Over Smartphone) [outbound] / Call not receive by agent [inbound]
	3. If customer did not answer -> Not received by seller / No answer
	4. Other statuses -> Busy / Cancelled / Failed / etc.

	Custom missed logic:
	- if status = missed and duration = 0 and billsec = 0 -> agent miss status
	- if status = missed and duration > 0 or billsec > 0 -> Not received by seller
	"""
	call_status = (payload.get("call_status") or "").strip().lower()

	end_dt = _extract_end(payload)
	answer_dt = _extract_answer(payload)

	billsec = _to_int(_pick(payload, ["billsec"]) or 0)
	duration = _to_int(_pick(payload, ["duration"]) or 0)

	call_connected = _extract_call_connected(payload)
	answered_agent = _extract_answered_agent(payload)
	missed_agent = _extract_missed_agent(payload)
	hangup_cause = _extract_hangup_cause(payload)
	reason_key = _pick(payload, ["reason_key", "hangup_cause_key"])

	hangup_cause_lower = str(hangup_cause).lower() if hangup_cause else ""
	reason_key_lower = str(reason_key).lower() if reason_key else ""

	agent_miss_status = (
		"Call not receive by agent (Over Smartphone)"
		if call_type == "outbound"
		else "Call not receive by agent"
	)

	frappe.logger().info(
		f"[SMARTFLOW STATUS MAPPING] call_status='{call_status}', "
		f"end_dt={end_dt}, answer_dt={answer_dt}, billsec={billsec}, duration={duration}, "
		f"call_connected={call_connected}, answered_agent='{answered_agent}', "
		f"missed_agent='{missed_agent}', hangup_cause='{hangup_cause}', reason_key='{reason_key}'"
	)

	# ---------------------------------------------------------
	# PRIORITY 1: another agent answered
	# ---------------------------------------------------------
	if answered_agent and (answer_dt or billsec > 0 or duration > 0 or call_connected):
		if end_dt:
			frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: Completed")
			return "Completed"
		frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: In Progress")
		return "In Progress"

	# ---------------------------------------------------------
	# PRIORITY 2: agent missed / rejected / cut before answer
	# ---------------------------------------------------------
	if missed_agent:
		frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: agent_miss_status (missed_agent)")
		return agent_miss_status

	if call_status in ("agent_missed", "agent_no_answer", "agent_not_answered", "agent_rejected"):
		frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: agent_miss_status (explicit call_status)")
		return agent_miss_status

	if any(k in hangup_cause_lower for k in ["agent rejected", "agent reject", "agent missed", "agent no answer", "agent not answered"]):
		frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: agent_miss_status (hangup cause)")
		return agent_miss_status

	if any(k in reason_key_lower for k in ["agent_rejected", "agent_missed", "agent_no_answer", "agent_not_answered"]):
		frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: agent_miss_status (reason_key)")
		return agent_miss_status

	# ---------------------------------------------------------
	# PRIORITY 3: missed = customer did not receive the call
	# Tata Tele sends call_status=missed when outgoing call is not answered by customer
	# ---------------------------------------------------------
	if call_status == "missed":
		frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: Not received by seller (missed)")
		return "Not received by seller"

	# ---------------------------------------------------------
	# duration present but no answer => customer did not receive
	# ---------------------------------------------------------
	if end_dt and not answer_dt and (billsec > 0 or duration > 0) and not answered_agent:
		frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: Not received by seller (duration but no answer)")
		return "Not received by seller"

	# ---------------------------------------------------------
	# zero duration, no answer, no connection => likely agent side miss
	# ---------------------------------------------------------
	if end_dt and not answer_dt and not call_connected and billsec <= 0 and duration <= 0:
		if "agent" in hangup_cause_lower or "agent" in reason_key_lower:
			frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: agent_miss_status (ended, no answer, agent-side reason)")
			return agent_miss_status

	# ---------------------------------------------------------
	# ringing
	# ---------------------------------------------------------
	if call_status in ("ringing", "agent_ringing"):
		frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: Ringing")
		return "Ringing"

	# ---------------------------------------------------------
	# connected / active
	# ---------------------------------------------------------
	if call_status in ("answered", "connected", "in_progress", "active"):
		if end_dt:
			frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: Completed")
			return "Completed"
		frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: In Progress")
		return "In Progress"

	# ---------------------------------------------------------
	# explicit ended/completed states
	# ---------------------------------------------------------
	if call_status in ("completed", "hangup", "ended", "disconnected"):
		if answered_agent and (answer_dt or call_connected or billsec > 0 or duration > 0):
			frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: Completed")
			return "Completed"

		if missed_agent:
			frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: agent_miss_status (completed block)")
			return agent_miss_status

		if "busy" in hangup_cause_lower:
			frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: Busy")
			return "Busy"

		if "cancel" in hangup_cause_lower or "user" in hangup_cause_lower:
			frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: Cancelled")
			return "Cancelled"

		if billsec > 0 or duration > 0:
			frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: Not received by seller")
			return "Not received by seller"

		frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: No answer")
		return "No answer"

	# ---------------------------------------------------------
	# explicit customer no answer statuses
	# ---------------------------------------------------------
	if call_status in ("no_answer", "not_answered"):
		frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: No answer")
		return "No answer"

	if call_status == "failed":
		frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: Failed")
		return "Failed"

	if call_status == "busy":
		frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: Busy")
		return "Busy"

	if call_status in ("cancelled", "canceled"):
		frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: Cancelled")
		return "Cancelled"

	# ---------------------------------------------------------
	# final heuristic when ended
	# ---------------------------------------------------------
	if end_dt:
		if answered_agent and (answer_dt or call_connected or billsec > 0 or duration > 0):
			frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: Completed (heuristic)")
			return "Completed"

		if missed_agent:
			frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: agent_miss_status (heuristic)")
			return agent_miss_status

		if "busy" in hangup_cause_lower:
			frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: Busy (heuristic)")
			return "Busy"

		if "cancel" in hangup_cause_lower or "user" in hangup_cause_lower:
			frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: Cancelled (heuristic)")
			return "Cancelled"

		if billsec > 0 or duration > 0:
			frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: Not received by seller (has duration, no answer)")
			return "Not received by seller"

		frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: No answer (default ended state)")
		return "No answer"

	if payload.get("answered_agent_number") or payload.get("answer_agent_number") or answered_agent:
		frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: In Progress")
		return "In Progress"

	frappe.logger().info("[SMARTFLOW STATUS MAPPING] Returning: Initiated")
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

		auth_header = (
			frappe.request.headers.get("Authorization")
			or frappe.request.headers.get("X-Auth-Token")
			or frappe.request.headers.get("X-Webhook-Token")
			or ""
		).strip()

		if not auth_header:
			frappe.logger().error("[SMARTFLOW AUTH] No authorization header found")
			headers_dict = {k: v for k, v in frappe.request.headers.items()}
			frappe.logger().error(f"[SMARTFLOW AUTH] All headers: {headers_dict}")
			return False

		received_token = auth_header

		if received_token.lower().startswith("bearer "):
			received_token = received_token[7:].strip()

		if received_token.lower().startswith("token "):
			received_token = received_token[6:].strip()

		if received_token == expected:
			frappe.logger().info("[SMARTFLOW AUTH] Token validated successfully")
			return True
		else:
			frappe.logger().error(
				f"[SMARTFLOW AUTH] Token mismatch - "
				f"Expected length: {len(expected)}, Received length: {len(received_token)}"
			)
			frappe.logger().error(f"[SMARTFLOW AUTH DEBUG] Expected token: {expected}")
			frappe.logger().error(f"[SMARTFLOW AUTH DEBUG] Received token: {received_token}")
			return False

	except Exception as e:
		frappe.logger().error(f"[SMARTFLOW AUTH] Exception: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "Smartflow Auth Error")
		return False


def _find_or_create_call_log(ref_id, agent_no=None, customer_no=None):
	"""
	tabCRM Call Log has UNIQUE column `id`.
	We store outbound ref_id in `id` so all webhook events update same row.
	Uses try/except on insert to prevent race-condition duplicates.
	"""
	name = frappe.db.get_value("CRM Call Log", {"id": ref_id}, "name")
	if name:
		return frappe.get_doc("CRM Call Log", name)

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
	data = {
		"ref_id": ref_id,
		"status": doc.status,
		"duration": doc.duration,
		"recording_url": doc.recording_url,
		"call_status": payload.get("call_status"),
		"call_id": _extract_call_id(payload),
		"receiver": doc.receiver,
		"note": doc.note,
	}
	frappe.publish_realtime("tata_tele_call", data)
	frappe.logger().info(f"[TATA TELE REALTIME] Published: {data}")


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

	if call_id:
		frappe.db.set_value("CRM Call Log", doc.name, "medium", f"Smartflow|{call_id}"[:140])
		frappe.db.commit()

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

@frappe.whitelist(allow_guest=True, methods=["POST"])
def webhook_handler():
	frappe.local.no_csrf = True

	print("\n" + "=" * 80)
	print("SMARTFLOW WEBHOOK RECEIVED")
	print("=" * 80)

	try:
		if not is_integration_enabled():
			print("❌ Integration not enabled")
			frappe.logger().warning("[SMARTFLOW] Integration not enabled")
			frappe.local.response.http_status_code = 503
			return {"success": False, "message": "Integration not enabled"}

		if not validate_webhook_token():
			print("❌ Webhook authentication FAILED")
			frappe.logger().error("[SMARTFLOW] Webhook authentication FAILED - returning 401")
			frappe.local.response.http_status_code = 401
			return {"success": False, "error": "Unauthorized", "message": "Invalid or missing webhook token"}

		print("✅ Webhook authenticated successfully")
		frappe.logger().info("[SMARTFLOW] Webhook authenticated successfully")

		payload = _get_json()

		# Log full webhook payload to frappe error log for easy debugging
		frappe.log_error(
			title="[SMARTFLOW] Webhook Payload Received",
			message=json.dumps(payload, indent=2)
		)

		print("\n" + "-" * 80)
		print("FULL WEBHOOK PAYLOAD:")
		print("-" * 80)
		print(json.dumps(payload, indent=2))
		print("-" * 80 + "\n")

		frappe.logger().info("[SMARTFLOW OUTBOUND WEBHOOK] Payload:\n" + json.dumps(payload, indent=2))

		ref_id = _extract_ref_id(payload)

		print(f"🔑 Extracted ref_id: {ref_id}")
		frappe.logger().info(f"[SMARTFLOW] Extracted ref_id: {ref_id}")
		frappe.logger().info(f"[SMARTFLOW] Payload keys: {list(payload.keys())}")

		if str(ref_id) == "$ref_id":
			ref_id = None

		if not ref_id:
			call_id = _extract_call_id(payload)
			if call_id and str(call_id) != "$call_id":
				frappe.logger().info(f"[SMARTFLOW RECOVERY] ref_id missing, searching by call_id={call_id}...")

				# 1. Try medium field (stored during make_a_call)
				matched = frappe.db.get_list(
					"CRM Call Log",
					filters={"medium": ["like", f"%{call_id}%"], "type": "Outgoing"},
					limit=1
				)
				if matched:
					ref_id = frappe.db.get_value("CRM Call Log", matched[0].name, "id")
					frappe.logger().info(f"[SMARTFLOW RECOVERY] Recovered via medium: {ref_id}")

				# 2. Try id = call_id directly
				if not ref_id:
					direct = frappe.db.get_value("CRM Call Log", {"id": call_id}, "id")
					if direct:
						ref_id = direct
						frappe.logger().info(f"[SMARTFLOW RECOVERY] Recovered via id match: {ref_id}")

				# 3. Try uuid field match
				if not ref_id:
					uuid_val = payload.get("uuid") or payload.get("UUID")
					if uuid_val:
						uuid_match = frappe.db.get_value("CRM Call Log", {"id": uuid_val}, "id")
						if uuid_match:
							ref_id = uuid_match
							frappe.logger().info(f"[SMARTFLOW RECOVERY] Recovered via uuid: {ref_id}")

				# 4. Last resort: use call_id as ref_id
				if not ref_id:
					ref_id = call_id
					frappe.logger().info(f"[SMARTFLOW RECOVERY] Using call_id as ref_id: {ref_id}")

		if not ref_id:
			print("⚠️ ref_id is MISSING and no call_id found - skipping")
			frappe.logger().warning("[SMARTFLOW] ref_id and call_id both missing, cannot process webhook.")
			call_type = payload.get("call_type") or payload.get("type") or payload.get("direction") or "unknown"
			return {
				"success": True,
				"message": "Webhook received but no identifier found",
				"call_type": call_type,
				"payload_keys": list(payload.keys())
			}

		agent_no = _extract_agent(payload)
		customer_no = _extract_customer(payload)

		answered_agent = _extract_answered_agent(payload)
		missed_agent = _extract_missed_agent(payload)
		hangup_cause = _extract_hangup_cause(payload)
		call_connected = _extract_call_connected(payload)

		doc = _find_or_create_call_log(ref_id, agent_no=agent_no, customer_no=customer_no)

		new_status = _map_status(payload, call_type="outbound")

		start_time = _extract_start(payload) or doc.start_time or frappe.utils.now_datetime()
		end_time = _extract_end(payload)
		duration = _extract_duration(payload)
		recording_url = _extract_recording(payload)
		call_id = _extract_call_id(payload)

		print(f"📄 Call Log: {doc.name}")
		print(f"📞 Agent Number: {agent_no}")
		print(f"📱 Customer Number: {customer_no}")
		print(f"👤 Answered Agent: {answered_agent}")
		print(f"❌ Missed Agent: {missed_agent}")
		print(f"📞 Hangup Cause: {hangup_cause}")
		print(f"🔗 Call Connected: {call_connected}")
		print(f"🎯 Mapped Status: {new_status}")

		updates = {"status": new_status}

		if agent_no:
			updates["from"] = _only_last_10(agent_no)

		if customer_no:
			updates["to"] = _only_last_10(customer_no)

		if not doc.start_time:
			updates["start_time"] = start_time

		# store actual answered agent in receiver field
		if answered_agent:
			updates["receiver"] = _safe_text(answered_agent, 140)

		# final state => end time
		if new_status in ("Completed", "No answer", "Call not receive by agent", "Call not receive by agent (Over Smartphone)", "Not received by seller", "Failed", "Busy", "Cancelled"):
			updates["end_time"] = end_time or frappe.utils.now_datetime()

		# duration
		if duration is not None and new_status in ("Completed", "No answer", "Call not receive by agent", "Call not receive by agent (Over Smartphone)", "Not received by seller"):
			updates["duration"] = duration

		# recording only on completed
		if recording_url and new_status == "Completed":
			updates["recording_url"] = recording_url

		# disconnect reason — save ONLY when call is Completed
		reason_key_val = payload.get("reason_key") or ""
		if new_status == "Completed" and reason_key_val:
			reason_lower = reason_key_val.strip().lower()
			if "callee" in reason_lower:
				disconnect_text = "Call disconnected by seller"
			elif "caller" in reason_lower:
				disconnect_text = "Call disconnected by agent"
			else:
				disconnect_text = reason_key_val[:140]

			# Use ref_id first (most reliable — call log id = ref_id)
			target_name = frappe.db.get_value("CRM Call Log", {"id": ref_id}, "name") if ref_id else None

			# Fallback: doc.name
			if not target_name and doc and doc.name:
				target_name = doc.name

			# Fallback: call_id
			if not target_name and call_id:
				target_name = frappe.db.get_value("CRM Call Log", {"id": call_id}, "name")

			if target_name:
				frappe.db.sql(
					"UPDATE `tabCRM Call Log` SET disconnect_reason = %s WHERE name = %s",
					(disconnect_text, target_name)
				)
				frappe.db.commit()
				frappe.logger().info(f"[SMARTFLOW] disconnect_reason='{disconnect_text}' saved for {target_name}")
			else:
				frappe.logger().warning(f"[SMARTFLOW] Could not save disconnect_reason. ref_id={ref_id} call_id={call_id}")

		print("\n" + "-" * 80)
		print("UPDATES TO APPLY:")
		print("-" * 80)
		print(json.dumps(updates, indent=2, default=str))
		print("-" * 80 + "\n")

		for k, v in updates.items():
			if k == "from":
				frappe.db.set_value("CRM Call Log", doc.name, "from", v)
			else:
				frappe.db.set_value("CRM Call Log", doc.name, k, v)

		frappe.db.commit()
		doc.reload()

		print(f"✅ FINAL Status in DB: {doc.status}")
		print(f"✅ FINAL Receiver in DB: {doc.receiver}")
		print(f"✅ FINAL Note in DB: {doc.note}")
		print(f"✅ FINAL Duration in DB: {doc.duration}")
		print(f"✅ FINAL End Time in DB: {doc.end_time}")
		print("=" * 80 + "\n")

		frappe.logger().info(
			f"[SMARTFLOW] Updates Applied - Final Status: {doc.status}, "
			f"Receiver: {doc.receiver}, Note: {doc.note}, Duration: {doc.duration}, End Time: {doc.end_time}"
		)

		_publish_realtime(ref_id, doc, payload)

		return {
			"success": True,
			"ref_id": ref_id,
			"status": doc.status,
			"receiver": doc.receiver,
			"note": doc.note,
			"duration": doc.duration,
			"recording_url": doc.recording_url,
		}

	except Exception as e:
		print(f"\n❌ EXCEPTION: {str(e)}")
		print(frappe.get_traceback())
		print("=" * 80 + "\n")

		frappe.logger().error(f"[SMARTFLOW] Exception in webhook_handler: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "Smartflow Webhook Error")
		frappe.local.response.http_status_code = 500
		return {
			"success": False,
			"error": "Internal server error",
			"message": str(e)
		}


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

	payload = {"call_id": call_id}

	try:
		resp = requests.post(url, json=payload, headers=headers, timeout=30)
	except Exception:
		frappe.log_error(frappe.get_traceback(), "Smartflo Hangup API Error")
		frappe.throw(_("Failed to connect to Tata Tele API"))

	if resp.status_code not in (200, 201):
		frappe.throw(_("Hangup failed: {0}").format(resp.text))

	data = resp.json() if resp.text else {}

	if ref_id:
		name = frappe.db.get_value("CRM Call Log", {"id": ref_id}, "name")
		if name:
			frappe.db.set_value("CRM Call Log", name, {
				"status": "Cancelled",
				"end_time": frappe.utils.now_datetime(),
				"note": "hangup_by_user"
			})
			frappe.db.commit()

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