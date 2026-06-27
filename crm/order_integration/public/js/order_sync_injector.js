// This script runs globally in the Frappe Desk
$(document).on('app_ready', function() {
    // Only proceed if we are on the specific site
    if (frappe.boot.sitename !== 'support2.localhost') return;

    // Use a Frappe UI Hook to inject into the CRM Dashboard/Settings
    // We wait for the CRM Settings page to be initialized
    frappe.ui.form.on('CRM Settings', {
        refresh: function(frm) {
            // Logic to add a custom button or tab dynamically
            frm.add_custom_button(__('Configure Order Sync'), () => {
                frappe.set_route('List', 'Order Sync Source');
            }, __('Integrations'));
        }
    });
});