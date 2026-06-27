frappe.ui.form.on('CRM Settings', {
    refresh: function(frm) {
        // Double check we are on the correct site
        if (frappe.boot.sitename === 'order.localhost') {
            
            // Add a dedicated section or button for Order Syncing
            frm.add_custom_button(__('Configure Order Syncing'), () => {
                // This routes the user to your custom DocType list
                frappe.set_route('List', 'Order Sync Source');
            }, __('Integrations'));

            // Optional: Highlighting the button
            frm.change_custom_button_type(__('Configure Order Syncing'), __('Integrations'), 'primary');
        }
    }
});