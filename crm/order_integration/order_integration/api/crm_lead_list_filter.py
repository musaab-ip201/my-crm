"""
CRM Lead List View Filter
Handles dynamic column filtering based on Order Source
"""

import frappe


def get_crm_lead_list_settings():
    """
    Get list view settings for CRM Lead with dynamic columns based on Order Source
    This is called by Frappe's list view rendering
    """
    return {
        "fields": [
            "`tabCRM Lead`.`name`",
            "`tabCRM Lead`.`owner`",
            "`tabCRM Lead`.`creation`",
            "`tabCRM Lead`.`modified`",
            "`tabCRM Lead`.`modified_by`",
            "`tabCRM Lead`.`_user_tags`",
            "`tabCRM Lead`.`_comments`",
            "`tabCRM Lead`.`_assign`",
            "`tabCRM Lead`.`_liked_by`",
            "`tabCRM Lead`.`docstatus`",
            "`tabCRM Lead`.`idx`",
            "`tabCRM Lead`.`status`",
            "`tabCRM Lead`.`converted`",
            "`tabCRM Lead`.`total`",
            "`tabCRM Lead`.`net_total`",
            "`tabCRM Lead`.`department_status`",
            "`tabCRM Lead`.`lead_name`",
            "`tabCRM Lead`.`image`",
            "`tabCRM Lead`.`current_department`",
            "`tabCRM Lead`.`order_source`",
            "current_department.stage_name as current_department_stage_name",
        ]
    }


@frappe.whitelist()
def get_filtered_columns(order_source=None):
    """
    Get columns to display based on Order Source filter
    Returns only columns relevant to the selected source
    """
    try:
        # Default columns always shown
        default_columns = [
            "name",
            "status",
            "email",
            "mobile_no",
            "assigned_to",
            "modified",
            "shift",
        ]

        if not order_source:
            # No filter selected - return only default columns
            return {"status": "success", "columns": default_columns, "api_columns": []}

        # Get API columns for this source
        api_columns = []
        try:
            # Get custom fields for this source
            custom_fields = frappe.get_all(
                "Custom Field",
                filters={
                    "dt": "CRM Lead",
                    "fieldname": [
                        "like",
                        f"api_col_{order_source.lower().replace('-', '_')}%",
                    ],
                },
                fields=["fieldname", "label"],
            )

            api_columns = [field["fieldname"] for field in custom_fields]
        except Exception as e:
            frappe.log_error(
                f"Error getting API columns: {str(e)}", "CRM Lead List Filter"
            )

        return {
            "status": "success",
            "columns": default_columns,
            "api_columns": api_columns,
        }

    except Exception as e:
        frappe.log_error(
            f"Error getting filtered columns: {str(e)}", "CRM Lead List Filter"
        )
        return {"status": "error", "message": str(e), "columns": [], "api_columns": []}
