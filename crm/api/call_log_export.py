import frappe
from crm.fcrm.doctype.crm_call_log.crm_call_log import export_call_logs_with_names

@frappe.whitelist()
def export_call_logs(filters=None, file_type="Excel"):
    """
    API endpoint to export call logs with proper caller and receiver names
    """
    return export_call_logs_with_names(filters=filters, file_type=file_type)

@frappe.whitelist()
def get_export_url():
    """
    Get the URL for custom call log export
    """
    return "/api/method/crm.api.call_log_export.export_call_logs"