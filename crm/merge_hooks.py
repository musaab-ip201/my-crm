# Script to merge lead_routing and order_integration hooks into main CRM hooks.py

import re

def merge_hooks():
    # Read current hooks
    with open('crm/hooks.py', 'r', encoding='utf-8') as f:
        hooks_content = f.read()

    # Additions for lead_routing
    lead_routing_additions = '''
# ═══════════════════════════════════════════════════════════════
# LEAD ROUTING INTEGRATION
# ═══════════════════════════════════════════════════════════════

# Lead Routing: Override CRM permission checks for department roles
on_session_creation = "lead_routing.api.crm_access.patch_crm_permission"

before_request_additions = ["lead_routing.api.crm_access.patch_crm_permission"]
'''

    # Additions for order_integration
    order_integration_additions = '''
# ═══════════════════════════════════════════════════════════════
# ORDER INTEGRATION
# ═══════════════════════════════════════════════════════════════

# Order Integration: Inject sidebar script
after_request_additions = ["order_integration.boot.inject_script_tag"]

# Order Integration: CRM Lead list view customization
app_include_js_additions = ["/assets/order_integration/js/crm_lead_list.js"]

# Order Integration: Override get_data method
override_whitelisted_methods_additions = {
    "crm.api.doc.get_data": "order_integration.api.override_get_data.get_data"
}
'''

    # Update doc_events for lead_routing
    doc_events_lead_routing = '''
	"CRM Lead": {
		"after_insert": [
			"crm.integrations.interakt.api.send_welcome_message_to_lead_hook",
			"lead_routing.api.lead_transfer.on_lead_created",  # NEW
		],
		"validate": [
			"lead_routing.api.lead_transfer.on_lead_validate",  # NEW
		],
	},
'''

    # Update permission_query_conditions for lead_routing
    permission_additions = '''
	"CRM Lead": "lead_routing.api.permissions.get_permission_query",  # NEW
'''

    # Update scheduler_events for order_integration
    scheduler_additions = '''
	"cron": {
		"*/1 * * * *": ["crm.lead_syncing.background_sync.sync_leads_from_sources_5_minutes"],
		"*/2 * * * *": ["crm.lead_syncing.background_sync.sync_leads_from_sources_2_minutes"],
		"*/5 * * * *": ["order_integration.doctype.order_sync_source.order_sync_source.run_scheduled_sync_by_frequency"],  # NEW
		"*/10 * * * *": [
			"crm.lead_syncing.background_sync.sync_leads_from_sources_10_minutes",
			"order_integration.doctype.order_sync_source.order_sync_source.run_scheduled_sync_by_frequency",  # NEW
		],
		"*/15 * * * *": ["crm.lead_syncing.background_sync.sync_leads_from_sources_15_minutes"],
		"0 * * * *": ["order_integration.doctype.order_sync_source.order_sync_source.run_scheduled_sync_by_frequency"],  # NEW (hourly)
		"0 0 * * *": ["order_integration.doctype.order_sync_source.order_sync_source.run_scheduled_sync_by_frequency"],  # NEW (daily)
	},
'''

    print("✅ Hooks configuration prepared!")
    print("\n📝 Manual Steps Required:")
    print("1. Edit crm/hooks.py")
    print("2. Add the integrations as shown in the guide")
    print("3. Commit to GitHub")
    print("4. Pull in Codespaces")
    print("5. Run bench migrate")

if __name__ == "__main__":
    merge_hooks()
