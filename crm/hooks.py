app_name = "crm"
app_title = "IP CRM"
app_publisher = "IP Technologies Pvt. Ltd."
app_description = "Kick-ass Open Source CRM"
app_email = "support.ipcrm@gmail.com"
app_license = "AGPLv3"
# ═══════════════════════════════════════════════════════════════
# LEAD ROUTING INTEGRATION
# ═══════════════════════════════════════════════════════════════

on_session_creation = "lead_routing.api.crm_access.patch_crm_permission"

app_icon_url = "/assets/crm/images/logo.svg"
app_icon_title = "CRM"
app_icon_route = "/crm"

# Apps
# ------------------

# required_apps = []
add_to_apps_screen = [
	{
		"name": "crm",
		"logo": "/assets/crm/images/logo.svg",
		"title": "CRM",
		"route": "/crm",
		"has_permission": "crm.api.check_app_permission",
	}
]

export_python_type_annotations = True

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/crm/css/crm.css"
app_include_js = ["/assets/order_integration/js/crm_lead_list.js"]  # ← NEW

# include js, css files in header of web template
# web_include_css = "/assets/crm/css/crm.css"
# web_include_js = "/assets/crm/js/crm.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "crm/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_list_js = {"CRM Call Log" : "public/js/call_log_export.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# "Role": "home_page"
# }

website_route_rules = [
	{"from_route": "/crm/<path:app_path>", "to_route": "crm"},
]

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# "methods": "crm.utils.jinja_methods",
# "filters": "crm.utils.jinja_filters"
# }

# Installation
# ------------

before_install = "crm.install.before_install"
after_install = "crm.install.after_install"

# Uninstallation
# ------------

before_uninstall = "crm.uninstall.before_uninstall"
# after_uninstall = "crm.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "crm.utils.before_app_install"
# after_app_install = "crm.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "crm.utils.before_app_uninstall"
# after_app_uninstall = "crm.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "crm.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
	"CRM Call Log": "crm.fcrm.doctype.crm_call_log.crm_call_log.get_permission_query_conditions",
	"CRM Lead": "lead_routing.api.permissions.get_permission_query",  # ← NEW
}


# has_permission = {
# "Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Contact": "crm.overrides.contact.CustomContact",
	"Email Template": "crm.overrides.email_template.CustomEmailTemplate",
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Contact": {
		"validate": ["crm.api.contact.validate"],
	},
	"ToDo": {
		"after_insert": ["crm.api.todo.after_insert"],
		"on_update": ["crm.api.todo.on_update"],
	},
	"Comment": {
		"on_update": ["crm.api.comment.on_update"],
	},
	"WhatsApp Message": {
		"validate": ["crm.api.whatsapp.validate"],
		"on_update": ["crm.api.whatsapp.on_update"],
	},
	"CRM WhatsApp Message": {
		"validate": ["crm.api.whatsapp.validate"],
		"on_update": ["crm.api.whatsapp.on_update"],
	},
	"CRM Lead": {
		"after_insert": [
			"crm.integrations.interakt.api.send_welcome_message_to_lead_hook",
			"lead_routing.api.lead_transfer.on_lead_created",  # ← NEW
		],
		"validate": [
			"lead_routing.api.lead_transfer.on_lead_validate",  # ← NEW
		],
	},
	# ... rest remains the same
	"CRM Deal": {
		"on_update": [
			"crm.fcrm.doctype.erpnext_crm_settings.erpnext_crm_settings.create_customer_in_erpnext"
		],
	},
	"User": {
		"before_validate": ["crm.api.demo.validate_user"],
		"validate_reset_password": ["crm.api.demo.validate_reset_password"],
	},
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": ["crm.api.event.trigger_offset_event_notifications"],
	"hourly": ["crm.api.event.trigger_hourly_event_notifications"],
	"daily": ["crm.api.event.trigger_daily_event_notifications"],
	"weekly": ["crm.api.event.trigger_weekly_event_notifications"],
	"daily_long": ["crm.lead_syncing.background_sync.sync_leads_from_sources_daily"],
	"hourly_long": ["crm.lead_syncing.background_sync.sync_leads_from_sources_hourly"],
	"monthly_long": ["crm.lead_syncing.background_sync.sync_leads_from_sources_monthly"],
	"cron": {
		"*/1 * * * *": ["crm.lead_syncing.background_sync.sync_leads_from_sources_5_minutes"],
		"*/2 * * * *": ["crm.lead_syncing.background_sync.sync_leads_from_sources_2_minutes"],
		"*/5 * * * *": ["order_integration.doctype.order_sync_source.order_sync_source.run_scheduled_sync_by_frequency"],  # ← NEW
		"*/10 * * * *": [
			"crm.lead_syncing.background_sync.sync_leads_from_sources_10_minutes",
			"order_integration.doctype.order_sync_source.order_sync_source.run_scheduled_sync_by_frequency",  # ← NEW
		],
		"*/15 * * * *": ["crm.lead_syncing.background_sync.sync_leads_from_sources_15_minutes"],
		"0 * * * *": ["order_integration.doctype.order_sync_source.order_sync_source.run_scheduled_sync_by_frequency"],  # ← NEW (hourly)
		"0 0 * * *": ["order_integration.doctype.order_sync_source.order_sync_source.run_scheduled_sync_by_frequency"],  # ← NEW (daily)
	},
}


# Testing
# -------

# before_tests = "crm.install.before_tests"

# Overriding Methods
# ------------------------------
#
# Overriding Methods
# ------------------------------
override_whitelisted_methods = {
	"crm.api.doc.get_data": "order_integration.api.override_get_data.get_data"  # ← NEW
}

#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# "Task": "crm.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

ignore_links_on_delete = ["Failed Lead Sync Log"]

# Request Events
# ----------------
before_request = ["lead_routing.api.crm_access.patch_crm_permission"]  # ← NEW
after_request = ["order_integration.boot.inject_script_tag"]  # ← NEW


# Job Events
# ----------
# before_job = ["crm.utils.before_job"]
# after_job = ["crm.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# {
# "doctype": "{doctype_1}",
# "filter_by": "{filter_by}",
# "redact_fields": ["{field_1}", "{field_2}"],
# "partial": 1,
# },
# {
# "doctype": "{doctype_2}",
# "filter_by": "{filter_by}",
# "partial": 1,
# },
# {
# "doctype": "{doctype_3}",
# "strict": False,
# },
# {
# "doctype": "{doctype_4}"
# }
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# "crm.auth.validate"
# ]

after_migrate = ["crm.fcrm.doctype.fcrm_settings.fcrm_settings.after_migrate"]

standard_dropdown_items = [
	{
		"name1": "app_selector",
		"label": "Apps",
		"type": "Route",
		"route": "#",
		"is_standard": 1,
	},
	{
		"name1": "toggle_theme",
		"label": "Toggle theme",
		"type": "Route",
		"icon": "moon",
		"route": "#",
		"is_standard": 1,
	},
	{
		"name1": "settings",
		"label": "Settings",
		"type": "Route",
		"icon": "settings",
		"route": "#",
		"is_standard": 1,
	},
	{
		"name1": "login_to_fc",
		"label": "Login to Frappe Cloud",
		"type": "Route",
		"route": "#",
		"is_standard": 1,
	},
	{
		"name1": "about",
		"label": "About",
		"type": "Route",
		"icon": "info",
		"route": "#",
		"is_standard": 1,
	},
	{
		"name1": "separator",
		"label": "",
		"type": "Separator",
		"is_standard": 1,
	},
	{
		"name1": "logout",
		"label": "Log out",
		"type": "Route",
		"icon": "log-out",
		"route": "#",
		"is_standard": 1,
	},
]
