// Custom export functionality for CRM Call Log
frappe.listview_settings['CRM Call Log'] = {
    onload: function(listview) {
        // Add permanent fix button
        listview.page.add_menu_item(__('Fix All Names (Permanent)'), function() {
            frappe.confirm(
                __('This will permanently update all call log records with proper caller and receiver names. This action cannot be undone. Continue?'),
                function() {
                    frappe.show_alert({
                        message: __('Fixing call log names...'),
                        indicator: 'blue'
                    });
                    
                    frappe.call({
                        method: 'crm.fcrm.doctype.crm_call_log.crm_call_log.fix_all_call_log_names',
                        callback: function(r) {
                            if (r.message && r.message.success) {
                                frappe.msgprint({
                                    title: __('Success'),
                                    message: r.message.message + '<br><br>' + 
                                            __('You can now export call logs with proper names using the standard Export button.'),
                                    indicator: 'green'
                                });
                                
                                // Refresh the list view to show updated data
                                listview.refresh();
                            } else {
                                frappe.msgprint({
                                    title: __('Error'),
                                    message: r.message ? r.message.message : __('Failed to fix call log names'),
                                    indicator: 'red'
                                });
                            }
                        },
                        error: function(r) {
                            frappe.msgprint({
                                title: __('Error'),
                                message: __('Failed to fix call log names. Please check the console for details.'),
                                indicator: 'red'
                            });
                        }
                    });
                }
            );
        });
        
        // Add custom export button (as backup)
        listview.page.add_menu_item(__('Custom Export (Excel)'), function() {
            let filters = listview.get_filters_for_args();
            
            frappe.call({
                method: 'crm.api.call_log_export.export_call_logs',
                args: {
                    filters: filters,
                    file_type: 'Excel'
                },
                callback: function(r) {
                    if (r.message) {
                        frappe.msgprint({
                            title: __('Export Complete'),
                            message: __('Call logs exported successfully with proper caller and receiver names.'),
                            indicator: 'green'
                        });
                    }
                }
            });
        });
    }
};