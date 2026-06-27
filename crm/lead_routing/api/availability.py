import frappe


@frappe.whitelist()
def toggle_availability():
    """
    Toggle the is_active field for the logged-in user across ALL
    Department Team Member child rows where they appear.

    Returns the NEW status string: "Available" or "Absent"
    """
    user = frappe.session.user

    # Fetch ALL rows for this user (a user can be in multiple departments)
    rows = frappe.get_all(
        "Department Team Member",
        filters={"user": user},
        fields=["name", "is_active"],
    )

    if not rows:
        frappe.throw(
            f"User {user} is not a member of any department team.",
            frappe.DoesNotExistError,
        )

    # Decide new status based on the FIRST row (all rows should be in sync)
    current_status = rows[0].is_active
    new_status = 0 if current_status else 1

    # Update every row for this user
    for row in rows:
        frappe.db.set_value(
            "Department Team Member",
            row.name,
            "is_active",
            new_status,
            update_modified=False,
        )

    # Update User Enabled checkbox as well
    frappe.db.set_value(
        "User",
        user,
        "enabled",
        new_status,
        update_modified=False,
    )

    frappe.db.commit()

    return "Available" if new_status else "Absent"


@frappe.whitelist()
def get_availability():
    """
    Return the current availability status of the logged-in user.
    Returns "Available", "Absent", or "not_a_member" if the user
    is not in any department team.
    """
    user = frappe.session.user

    row = frappe.db.get_value(
        "Department Team Member",
        {"user": user},
        "is_active",
    )

    # row is None  → user not in any team
    # row is 0/1   → their current status
    if row is None:
        return "not_a_member"

    return "Available" if row else "Absent"
