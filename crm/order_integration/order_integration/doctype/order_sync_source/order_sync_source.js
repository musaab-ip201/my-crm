// Copyright (c) 2026, aakansha and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Order Sync Source", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Order Sync Source', {
    refresh: function(frm) {
        // Add a primary button to trigger the sync manually
        if (frm.doc.enabled) {
            frm.add_custom_button(__('Sync Now'), function() {
                frm.call('sync_now').then(r => {
                    if (r.message) {
                        frappe.msgprint(r.message);
                    }
                });
            }).addClass('btn-primary');
        }
    }
});