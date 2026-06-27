app_name = "order_integration"
app_title = "Order Integration"
app_publisher = "aakansha"
app_description = "Sync orders from external APIs and convert to leads"
app_email = "aakanshaaghav6@gmail.com"
app_license = "mit"

# Setup after installation
after_install = "order_integration.setup.after_install"

# Inject sidebar script into /crm page via after_request hook.
# app_include_js does NOT work for /crm — it's a standalone HTML template,
# not a Frappe desk page. after_request intercepts the HTML response and
# inserts our <script> tag before </body>.
after_request = ["order_integration.boot.inject_script_tag"]

# Include JS files for CRM Lead list view customization
app_include_js = [ "/assets/order_integration/js/crm_lead_list.js" ]

# Scheduled Tasks
scheduler_events = {
    "cron": {
        # Every 5 minutes
        "*/5 * * * *": [
            "order_integration.doctype.order_sync_source.order_sync_source.run_scheduled_sync_by_frequency"
        ],
        # Every 10 minutes
        "*/10 * * * *": [
            "order_integration.doctype.order_sync_source.order_sync_source.run_scheduled_sync_by_frequency"
        ],
        # Every hour
        "0 * * * *": [
            "order_integration.doctype.order_sync_source.order_sync_source.run_scheduled_sync_by_frequency"
        ],
        # Every day at midnight
        "0 0 * * *": [
            "order_integration.doctype.order_sync_source.order_sync_source.run_scheduled_sync_by_frequency"
        ]
    }
}

export_python_type_annotations = True

override_whitelisted_methods = {
    "crm.api.doc.get_data": "order_integration.api.override_get_data.get_data"
}
