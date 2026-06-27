# Copyright (c) 2026, IP CRM and contributors
# For license information, please see license.txt

"""
Lead history API — role-based views:
  • Non-admin users see leads they previously acted on (exited department log entries).
  • Admin / System Manager users see all completed/rejected leads globally,
    or a specific user's history when the `user` filter is set.
"""

import frappe
from frappe.utils import get_fullname


def _is_admin():
    """Check if the current session user is Administrator or System Manager."""
    roles = frappe.get_roles(frappe.session.user)
    return "Administrator" in roles or "System Manager" in roles


def _is_department_manager():
    """Check if the current user is a department manager."""
    user_roles = frappe.get_roles(frappe.session.user)
    dept_stages = frappe.get_all(
        "Department Pipeline Stage",
        filters={"enabled": 1},
        fields=["manager_role"],
    )
    for stage in dept_stages:
        if stage.manager_role and stage.manager_role in user_roles:
            return True
    return False


def _get_user_department_stages(user=None):
    """Get the department stages that a user has access to based on their roles."""
    check_user = user or frappe.session.user
    if check_user in ("Administrator", "Guest"):
        return []
    
    user_roles = frappe.get_roles(check_user)
    dept_stages = frappe.get_all(
        "Department Pipeline Stage",
        filters={"enabled": 1},
        fields=["name", "stage_name", "department_role", "manager_role"],
    )
    
    user_stage_names = []
    for stage in dept_stages:
        if (stage.department_role and stage.department_role in user_roles) or \
           (stage.manager_role and stage.manager_role in user_roles):
            user_stage_names.append(stage.name)
    
    return user_stage_names


def _filter_leads_by_user_access(leads_data, user=None):
    """Filter leads based on user's department stage access."""
    check_user = user or frappe.session.user
    
    # Admins and department managers see everything
    if _is_admin() or _is_department_manager():
        return leads_data
    
    # Get user's accessible department stages
    user_stages = _get_user_department_stages(check_user)
    
    if not user_stages:
        # User has no department stages assigned, return empty
        return []
    
    # Filter leads to only show those from user's accessible departments
    filtered_leads = []
    for lead in leads_data:
        # Check if lead's current department is in user's accessible stages
        if lead.get("current_department") in user_stages:
            filtered_leads.append(lead)
            continue
            
        # Also check if user has handled this lead in any of their departments
        lead_logs = frappe.get_all(
            "Lead Department Log",
            filters={
                "parent": lead.name,
                "parenttype": "CRM Lead",
                "department": ("in", user_stages),
                "assigned_user": check_user
            },
            fields=["name"],
            limit=1
        )
        
        # If user has handled this lead in their departments, include it
        if lead_logs:
            filtered_leads.append(lead)
    
    return filtered_leads


def _get_user_perspective_status(lead, user_entry, current_department_status):
    """
    Determine what status to show from the user's perspective based on their action
    and the current state of the lead.
    """
    user_action = user_entry.get("last_action") or user_entry.get("action")
    has_exited = user_entry.get("exited_at") is not None
    
    # Debug logging
    frappe.log_error(f"Status Debug - Lead: {lead.get('name')}, Action: {user_action}, Exited: {has_exited}, Current Status: {current_department_status}", "Lead Status Debug")
    
    # If user hasn't exited the department yet, they're still working on it
    if not has_exited:
        return "Working"
    
    # Based on the action they took when exiting
    if user_action == "Forward":
        # Check if the lead is still in progress or completed
        if current_department_status in ["Done", "Completed"]:
            return "Completed"
        else:
            return "Transferred"
    
    elif user_action == "Backward":
        return "Sent Back"
    
    elif user_action == "Reject":
        return "Rejected"
    
    elif user_action == "Manager Override":
        return "Overridden"
    
    elif user_action == "Initial":
        # Initial assignment, check current status
        if current_department_status == "Working":
            return "Assigned"
        elif current_department_status in ["Done", "Completed"]:
            return "Completed"
        else:
            return "Processed"
    
    # Fallback to current department status
    return current_department_status or "Unknown"


def _get_personal_history(user):
    """
    Return leads that `user` has been assigned to work on — i.e. Lead Department Log
    entries where assigned_user == user. Shows all leads the user has handled,
    regardless of whether they've completed them or not.
    Each lead includes its current_department so the user can see where
    the lead is now after they handled it.
    
    For regular department users: only shows leads from their department/shift.
    For managers and admins: shows all leads they've handled.
    """
    history_entries = frappe.get_all(
        "Lead Department Log",
        filters={
            "assigned_user": user,
            "parenttype": "CRM Lead",
        },
        fields=["parent", "department", "entered_at", "exited_at", "action", "last_action"],
        order_by="parent, entered_at desc",
    )

    if not history_entries:
        return {
            "leads": [],
            "user": user,
            "full_name": get_fullname(user),
            "view_type": "personal",
        }

    # Deduplicate leads — keep the most recent log action per lead
    seen = {}
    for h in history_entries:
        if h.parent not in seen:
            seen[h.parent] = h

    lead_names = list(seen.keys())

    leads_data = frappe.get_all(
        "CRM Lead",
        filters={"name": ("in", lead_names)},
        fields=[
            "name", "lead_name", "email", "mobile_no",
            "current_department", "department_status", "status",
            "modified",
        ],
        order_by="modified desc",
        ignore_permissions=True,
    )

    # Apply department/shift filtering for regular users
    leads_data = _filter_leads_by_user_access(leads_data, user)

    # Enrich each lead with the action the user performed and user-perspective status
    for lead in leads_data:
        entry = seen.get(lead.name)
        if entry:
            lead["user_action"] = entry.last_action or entry.action
            lead["action_department"] = entry.department
            lead["action_at"] = str(entry.exited_at) if entry.exited_at else str(entry.entered_at)
            
            # Set user-perspective status instead of just department_status
            lead["user_perspective_status"] = _get_user_perspective_status(
                lead, entry, lead.get("department_status")
            )

    return {
        "leads": leads_data,
        "user": user,
        "full_name": get_fullname(user),
        "view_type": "personal",
    }


def _get_global_history():
    """
    Admin global view — all leads that have been routed (have department log entries).
    Shows all lead transfers and routing history, not just completed ones.
    Each lead is enriched with who last handled it and the last *meaningful*
    transition action (not just the latest 'Initial' on the newest dept entry).
    
    For regular department users: only shows leads from their department/shift.
    For managers and admins: shows all routed leads.
    """
    # Get all leads that have department log entries (i.e., have been routed)
    routed_lead_names = frappe.db.sql("""
        SELECT DISTINCT parent 
        FROM `tabLead Department Log` 
        WHERE parenttype = 'CRM Lead'
    """, pluck=True)
    
    if not routed_lead_names:
        return {
            "leads": [],
            "view_type": "global",
            "done_count": 0,
            "rejected_count": 0,
            "working_count": 0,
            "total_routed": 0,
        }
    
    leads_data = frappe.get_all(
        "CRM Lead",
        filters={"name": ("in", routed_lead_names)},
        fields=[
            "name", "lead_name", "email", "mobile_no",
            "current_department", "department_status", "status",
            "modified",
        ],
        order_by="modified desc",
        ignore_permissions=True,
    )

    if not leads_data:
        return {
            "leads": [],
            "view_type": "global",
            "done_count": 0,
            "rejected_count": 0,
            "working_count": 0,
            "total_routed": 0,
        }

    # Apply department/shift filtering for regular users
    leads_data = _filter_leads_by_user_access(leads_data)

    lead_names = [l.name for l in leads_data]

    # Fetch ALL department log entries for these leads, ordered newest first
    all_logs = frappe.get_all(
        "Lead Department Log",
        filters={
            "parent": ("in", lead_names),
            "parenttype": "CRM Lead",
        },
        fields=["parent", "assigned_user", "action", "last_action", "department", "exited_at", "entered_at"],
        order_by="parent, entered_at desc",
    )

    # Build two maps per lead:
    #  1. latest_log: the most recent log entry (for current handler info)
    #  2. last_transition_log: the most recent *exited* entry with a transition
    #     action (Forward/Backward/Reject/Manager Override) for meaningful action display
    latest_log = {}
    last_transition_log = {}
    for log in all_logs:
        if log.parent not in latest_log:
            latest_log[log.parent] = log

        # Find the most recent log with a real transition action
        if log.parent not in last_transition_log:
            transition_action = log.last_action or (log.action if log.action != "Initial" else None)
            if transition_action and transition_action != "Initial":
                last_transition_log[log.parent] = log

    for lead in leads_data:
        log = latest_log.get(lead.name)
        transition_log = last_transition_log.get(lead.name)

        if log:
            lead["last_handled_by"] = log.assigned_user
            lead["last_handled_by_name"] = get_fullname(log.assigned_user) if log.assigned_user else "—"
        else:
            lead["last_handled_by"] = None
            lead["last_handled_by_name"] = "—"

        # Prefer the real transition action; fall back to the latest log's action
        if transition_log:
            lead["last_action"] = transition_log.last_action or transition_log.action
        elif log:
            lead["last_action"] = log.last_action or log.action
        else:
            lead["last_action"] = None

    # Compute counts for stat cards
    done_count = sum(1 for l in leads_data if l.department_status == "Done")
    rejected_count = sum(1 for l in leads_data if l.department_status == "Rejected")
    working_count = sum(1 for l in leads_data if l.department_status == "Working")
    total_routed = len(leads_data)

    return {
        "leads": leads_data,
        "done_count": done_count,
        "rejected_count": rejected_count,
        "working_count": working_count,
        "total_routed": total_routed,
        "view_type": "global",
    }


@frappe.whitelist()
def get_users_with_lead_history():
    """
    Get all users who have handled leads (have entries in Lead Department Log)
    plus all CRM users, to show in the Lead History sidebar.
    
    For regular department users: only shows users from their accessible departments.
    For managers and admins: shows all users.
    """
    current_user = frappe.session.user
    
    # Admins and department managers see all users
    if _is_admin() or _is_department_manager():
        # Get users who have handled leads (exclude system accounts)
        users_with_history = frappe.db.sql("""
            SELECT DISTINCT assigned_user as name
            FROM `tabLead Department Log` 
            WHERE assigned_user IS NOT NULL
            AND assigned_user NOT IN ('Administrator', 'Guest')
        """, as_dict=True)
        
        # Get all CRM users (from CRM app)
        try:
            from crm.api.user import get_crm_users
            crm_users_response = get_crm_users()
            crm_users = crm_users_response.get('crmUsers', [])
        except:
            # Fallback: get all active users
            crm_users = frappe.get_all(
                "User",
                filters={"enabled": 1, "user_type": "System User"},
                fields=["name", "full_name", "user_image"],
                order_by="full_name"
            )
        
        # Combine and deduplicate users
        all_user_names = set()
        
        # Add users who have handled leads
        for user in users_with_history:
            if user.name:
                all_user_names.add(user.name)
        
        # Add all CRM users
        for user in crm_users:
            all_user_names.add(user.get('name'))
    
    else:
        # Regular department users only see users from their accessible departments
        user_stages = _get_user_department_stages(current_user)
        
        if not user_stages:
            return {"users": []}
        
        # Get users who have the same department roles
        dept_stages = frappe.get_all(
            "Department Pipeline Stage",
            filters={"name": ("in", user_stages)},
            fields=["department_role", "manager_role"],
        )
        
        accessible_roles = set()
        for stage in dept_stages:
            if stage.department_role:
                accessible_roles.add(stage.department_role)
            if stage.manager_role:
                accessible_roles.add(stage.manager_role)
        
        if not accessible_roles:
            return {"users": []}
        
        # Get users with the same roles
        users_with_roles = frappe.db.sql("""
            SELECT DISTINCT u.name
            FROM `tabUser` u
            JOIN `tabHas Role` hr ON hr.parent = u.name
            WHERE hr.role IN %s
            AND u.enabled = 1
            AND u.user_type = 'System User'
        """, (list(accessible_roles),), as_dict=True)
        
        all_user_names = {u.name for u in users_with_roles}
        
        # Also include users who have handled leads in the same departments
        users_with_history = frappe.db.sql("""
            SELECT DISTINCT assigned_user as name
            FROM `tabLead Department Log` 
            WHERE assigned_user IS NOT NULL
            AND department IN %s
        """, (user_stages,), as_dict=True)
        
        for user in users_with_history:
            if user.name:
                all_user_names.add(user.name)
    
    # Remove system accounts from the list
    all_user_names.discard("Administrator")
    all_user_names.discard("Guest")

    # Get full user details
    if all_user_names:
        users_list = frappe.get_all(
            "User",
            filters={"name": ("in", list(all_user_names)), "enabled": 1},
            fields=["name", "full_name", "user_image"],
            order_by="full_name"
        )
    else:
        users_list = []
    
    return {"users": users_list}


@frappe.whitelist()
def get_my_lead_history(user=None):
    """
    Main entry point — returns role-appropriate lead history.
    
    For regular department users: only shows leads from their department/shift.
    For managers and admins: shows all leads or specific user history.
    """
    current_user = frappe.session.user
    is_admin = _is_admin()
    is_manager = _is_department_manager()

    # Non-admin/non-manager requesting another user's history → deny
    if user and user != current_user and not (is_admin or is_manager):
        frappe.throw("You do not have permission to view other users' lead history.")

    # Admin/Manager with a user filter → personal history for that user
    if (is_admin or is_manager) and user:
        return _get_personal_history(user)

    # Admin/Manager without user filter → global view
    if (is_admin or is_manager) and not user:
        return _get_global_history()

    # Regular department user → personal history only (filtered by their dept/shift)
    return _get_personal_history(current_user)


@frappe.whitelist()
def get_lead_department_history(lead_name):
    """
    Returns the full department transition history for a specific lead.
    """
    frappe.has_permission("CRM Lead", doc=lead_name, ptype="read", throw=True)

    history = frappe.get_all(
        "Lead Department Log",
        filters={
            "parent": lead_name,
            "parenttype": "CRM Lead",
        },
        fields=[
            "department", "shift", "entered_at", "exited_at",
            "action", "assigned_user",
        ],
        order_by="entered_at asc",
    )

    # Add full names
    for entry in history:
        if entry.assigned_user:
            entry["assigned_user_name"] = get_fullname(entry.assigned_user)

    return history


@frappe.whitelist()
def check_admin_assignments():
    """Debug function to check Administrator assignments"""
    # Check if Administrator has any lead assignments
    assignments = frappe.db.sql("""
        SELECT parent, department, action, assigned_user, entered_at, exited_at
        FROM `tabLead Department Log` 
        WHERE assigned_user = 'Administrator'
        ORDER BY entered_at DESC
    """, as_dict=True)
    
    return {
        "log_entries": assignments,
        "log_count": len(assignments)
    }

@frappe.whitelist()
def export_lead_history_to_excel(user=None, filters=None):
	"""
	Export lead history data to Excel format.
	
	Args:
		user: Optional user filter for personal history
		filters: JSON string containing filter criteria (action, search, date_from, date_to)
	"""
	import json
	from frappe.utils.xlsxutils import make_xlsx
	from frappe.utils import format_datetime
	
	# Parse filters if provided
	filter_data = {}
	if filters:
		try:
			filter_data = json.loads(filters)
		except:
			filter_data = {}
	
	# Get the lead history data using existing function
	history_data = get_my_lead_history(user)
	leads = history_data.get('leads', [])
	view_type = history_data.get('view_type', 'personal')
	
	# Apply client-side filters (same logic as frontend)
	filtered_leads = leads
	
	# Filter by action
	if filter_data.get('action'):
		filtered_leads = [l for l in filtered_leads if (l.get('last_action') or l.get('user_action')) == filter_data['action']]
	
	# Filter by search query
	if filter_data.get('search'):
		search_query = filter_data['search'].lower()
		filtered_leads = [
			l for l in filtered_leads 
			if (l.get('name', '').lower().find(search_query) >= 0 or 
				l.get('lead_name', '').lower().find(search_query) >= 0)
		]
	
	# Filter by date range
	if filter_data.get('date_from'):
		from frappe.utils import getdate
		date_from = getdate(filter_data['date_from'])
		filtered_leads = [l for l in filtered_leads if getdate(l.get('modified', '')) >= date_from]
	
	if filter_data.get('date_to'):
		from frappe.utils import getdate
		date_to = getdate(filter_data['date_to'])
		filtered_leads = [l for l in filtered_leads if getdate(l.get('modified', '')) <= date_to]
	
	# Prepare data for Excel
	data = []
	
	# Define column headers based on view type
	if view_type == 'global':
		headers = [
			"Lead ID", "Lead Name", "Email", "Mobile No", 
			"Department", "Status", "Last Action", "Last Handled By", "Last Updated"
		]
	else:
		headers = [
			"Lead ID", "Lead Name", "Email", "Mobile No", 
			"Department", "Status", "Action Taken", "Last Updated"
		]
	
	# Add headers as first row
	data.append(headers)
	
	# Add data rows
	for lead in filtered_leads:
		# Determine status based on view type
		if view_type == 'personal':
			user_action = lead.get('user_action') or lead.get('last_action')
			if user_action == 'Forward':
				status = 'Transferred'
			elif user_action == 'Backward':
				status = 'Sent Back'
			elif user_action == 'Reject':
				status = 'Rejected'
			elif user_action == 'Manager Override':
				status = 'Overridden'
			elif user_action == 'Initial':
				status = 'Assigned'
			else:
				status = 'Working'
		else:
			status = lead.get('department_status') or lead.get('status', 'Working')
		
		if view_type == 'global':
			row = [
				lead.get('name', ''),
				lead.get('lead_name', ''),
				lead.get('email', ''),
				lead.get('mobile_no', ''),
				lead.get('current_department', ''),
				status,
				lead.get('last_action', ''),
				lead.get('last_handled_by_name', ''),
				format_datetime(lead.get('modified', '')) if lead.get('modified') else ''
			]
		else:
			row = [
				lead.get('name', ''),
				lead.get('lead_name', ''),
				lead.get('email', ''),
				lead.get('mobile_no', ''),
				lead.get('current_department', ''),
				status,
				lead.get('user_action') or lead.get('last_action', ''),
				format_datetime(lead.get('modified', '')) if lead.get('modified') else ''
			]
		data.append(row)
	
	# Generate filename
	from frappe.utils import now_datetime
	timestamp = now_datetime().strftime("%Y%m%d_%H%M%S")
	view_label = "Global" if view_type == 'global' else "Personal"
	filename = f"Lead_History_{view_label}_{timestamp}.xlsx"
	
	# Create Excel file using make_xlsx with proper data structure
	xlsx_data = make_xlsx(data, "Lead History")
	
	# Return file data
	frappe.response['filename'] = filename
	frappe.response['filecontent'] = xlsx_data.getvalue()
	frappe.response['type'] = 'binary'