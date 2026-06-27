# order_integration/api/customer_assignment.py
"""
Assign a CRM Lead to the correct Department Pipeline Stage based on the
Order Sync Source's source_type.

  source_type contains "cart"   → Customer-side department (stage_name contains "customer")
  source_type contains "ticket" → Seller-side department   (stage_name contains "seller")
  fallback                      → first enabled stage

Uses lead_routing's _assign_to_least_loaded for round-robin assignment.
"""

import frappe
from lead_routing.api.lead_transfer import (
    _assign_to_least_loaded,
    _update_lead_department_safely,
    _get_shift_for_time,
)


def _find_stage_for_source_type(source_type: str):
    """
    Return the best-matching Department Pipeline Stage for a given source_type.

    Matching priority:
    1. stage_name contains "seller"  when source_type contains "ticket"
    2. stage_name contains "customer" when source_type contains "cart"
    3. First enabled stage as fallback
    """
    all_stages = frappe.get_all(
        "Department Pipeline Stage",
        filters={"enabled": 1},
        fields=["name", "stage_name"],
        order_by="stage_order ASC",
    )

    if not all_stages:
        frappe.log_error(
            title="Customer Assignment",
            message="No enabled Department Pipeline Stages found",
        )
        return None

    source_lower = (source_type or "").lower()

    # Determine keyword to search for in stage_name
    if "seller" in source_lower:
        keyword = "seller"
    elif "customer" in source_lower:
        keyword = "customer"
    elif "ticket" in source_lower:
        keyword = "seller"
    elif "cart" in source_lower:
        keyword = "customer"
    else:
        keyword = None

    if keyword:
        for stage in all_stages:
            if keyword in stage.stage_name.lower():
                return frappe.get_doc("Department Pipeline Stage", stage.name)

    # Fallback: first enabled stage
    return frappe.get_doc("Department Pipeline Stage", all_stages[0].name)


def assign_by_source_department(lead_id: str, source_name: str) -> bool:
    """
    Assign a newly-created lead to the correct department based on the
    Order Sync Source's source_type.

    Returns True on success, False on failure.
    """
    try:
        source = frappe.get_doc("Order Sync Source", source_name)
        source_type = source.source_type or ""

        stage = _find_stage_for_source_type(source_type)
        if not stage:
            frappe.log_error(
                title="Customer Assignment",
                message=f"No matching stage for source_type='{source_type}' (source: {source_name})",
            )
            return False

        # Determine shift
        shift = _get_shift_for_time(frappe.utils.now_datetime())
        shift_name = shift.name if shift else None

        # Update lead routing fields safely (bypasses on_lead_validate guard)
        lead = frappe.get_doc("CRM Lead", lead_id)
        _update_lead_department_safely(lead, stage.name, "Working")

        # Insert department history log
        frappe.get_doc({
            "doctype": "Lead Department Log",
            "parent": lead_id,
            "parenttype": "CRM Lead",
            "parentfield": "department_history",
            "department": stage.name,
            "shift": shift_name,
            "entered_at": frappe.utils.now_datetime(),
            "action": "Initial",
        }).insert(ignore_permissions=True)

        frappe.db.commit()

        # Reload so _assign_to_least_loaded sees the fresh state
        lead.reload()
        _assign_to_least_loaded(lead, stage)

        frappe.log_error(
            title="Customer Assignment",
            message=f"Lead {lead_id} assigned to stage '{stage.stage_name}' (source_type={source_type})",
        )
        return True

    except Exception:
        frappe.log_error(
            title="Customer Assignment Error",
            message=frappe.get_traceback(),
        )
        return False
