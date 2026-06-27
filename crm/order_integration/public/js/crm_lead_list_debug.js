// CRM Lead List Debug Script
// Provides debugging functions to test column filtering

(function() {
    
    // Expose debug functions globally
    window.debugCRMLeadColumns = {
        
        // Get all API columns from database
        getAllApiColumns: function() {
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Custom Field',
                    filters: {
                        dt: 'CRM Lead',
                        fieldname: ['like', 'api_col_%']
                    },
                    fields: ['fieldname', 'description', 'label'],
                    limit_page_length: 500
                },
                callback: function(r) {
                    console.log('=== ALL API COLUMNS ===');
                    if (r.message) {
                        console.table(r.message);
                        console.log('Total columns:', r.message.length);
                    } else {
                        console.log('No API columns found');
                    }
                }
            });
        },
        
        // Get current filter state
        getCurrentFilters: function() {
            if (typeof cur_list === 'undefined' || !cur_list) {
                console.log('cur_list not available');
                return;
            }
            
            const filters = cur_list.filter_area?.get() || [];
            console.log('=== CURRENT FILTERS ===');
            console.table(filters);
            
            const orderSourceFilter = filters.find(f => f[1] === 'order_source');
            console.log('Order Source Filter:', orderSourceFilter);
            
            return filters;
        },
        
        // Get columns in current list view
        getListViewColumns: function() {
            if (typeof cur_list === 'undefined' || !cur_list) {
                console.log('cur_list not available');
                return;
            }
            
            console.log('=== LIST VIEW COLUMNS ===');
            console.log('Fields:', cur_list.fields);
            console.log('Data:', cur_list.data);
            
            // Check DOM for column headers
            const headers = document.querySelectorAll('.list-row-col');
            console.log('DOM Column Headers:', headers.length);
            headers.forEach(h => {
                console.log('  -', h.getAttribute('data-field'), h.getAttribute('data-fieldname'));
            });
        },
        
        // Test CSS application
        testCSSApplication: function() {
            console.log('=== TESTING CSS APPLICATION ===');
            
            // Create test style
            const styleEl = document.createElement('style');
            styleEl.id = 'test-column-filter';
            styleEl.textContent = `
                .list-row-col[data-field="api_col_test"] { 
                    background-color: red !important; 
                }
            `;
            document.head.appendChild(styleEl);
            
            console.log('Test style applied. Check if any columns turn red.');
            console.log('If no columns turn red, the CSS selectors are not matching the DOM.');
        },
        
        // Get all custom fields on CRM Lead
        getAllCustomFields: function() {
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Custom Field',
                    filters: {
                        dt: 'CRM Lead'
                    },
                    fields: ['fieldname', 'label', 'description'],
                    limit_page_length: 500
                },
                callback: function(r) {
                    console.log('=== ALL CUSTOM FIELDS ON CRM LEAD ===');
                    if (r.message) {
                        console.table(r.message);
                        console.log('Total fields:', r.message.length);
                    }
                }
            });
        },
        
        // Check if order_source field exists
        checkOrderSourceField: function() {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Custom Field',
                    name: 'CRM Lead-order_source'
                },
                callback: function(r) {
                    if (r.message) {
                        console.log('=== ORDER SOURCE FIELD ===');
                        console.table(r.message);
                    } else {
                        console.log('Order Source field NOT found');
                    }
                }
            });
        },
        
        // Manually trigger column filtering
        manuallyFilterColumns: function() {
            console.log('=== MANUALLY FILTERING COLUMNS ===');
            
            if (typeof cur_list === 'undefined' || !cur_list) {
                console.log('cur_list not available');
                return;
            }
            
            const filters = cur_list.filter_area?.get() || [];
            const orderSourceFilter = filters.find(f => f[1] === 'order_source');
            const selectedSource = orderSourceFilter ? orderSourceFilter[2] : null;
            
            console.log('Selected Order Source:', selectedSource);
            
            // Get all API columns
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Custom Field',
                    filters: {
                        dt: 'CRM Lead',
                        fieldname: ['like', 'api_col_%']
                    },
                    fields: ['fieldname', 'description'],
                    limit_page_length: 500
                },
                callback: function(r) {
                    if (!r.message) {
                        console.log('No API columns found');
                        return;
                    }
                    
                    const sourceColumnMap = {};
                    r.message.forEach(cf => {
                        if (cf.description && cf.description.includes('api_source:')) {
                            const source = cf.description.split('api_source:')[1].trim();
                            if (!sourceColumnMap[source]) {
                                sourceColumnMap[source] = [];
                            }
                            sourceColumnMap[source].push(cf.fieldname);
                        }
                    });
                    
                    console.log('Source Column Map:', sourceColumnMap);
                    
                    const columnsToShow = selectedSource ? (sourceColumnMap[selectedSource] || []) : [];
                    console.log('Columns to show:', columnsToShow);
                    
                    // Apply CSS
                    let styleEl = document.getElementById('crm-lead-api-column-filter');
                    if (styleEl) {
                        styleEl.remove();
                    }
                    
                    styleEl = document.createElement('style');
                    styleEl.id = 'crm-lead-api-column-filter';
                    
                    let css = '';
                    r.message.forEach(cf => {
                        css += `.list-row-col[data-field="${cf.fieldname}"] { display: none !important; }\n`;
                    });
                    
                    columnsToShow.forEach(colName => {
                        css += `.list-row-col[data-field="${colName}"] { display: table-cell !important; }\n`;
                    });
                    
                    styleEl.textContent = css;
                    document.head.appendChild(styleEl);
                    
                    console.log('CSS applied. Check if columns are now visible/hidden.');
                }
            });
        },
        
        // Print all available debug functions
        help: function() {
            console.log(`
=== CRM LEAD COLUMNS DEBUG FUNCTIONS ===

window.debugCRMLeadColumns.getAllApiColumns()
  - Get all API columns from database

window.debugCRMLeadColumns.getCurrentFilters()
  - Get current filter state

window.debugCRMLeadColumns.getListViewColumns()
  - Get columns in current list view

window.debugCRMLeadColumns.testCSSApplication()
  - Test if CSS selectors work

window.debugCRMLeadColumns.getAllCustomFields()
  - Get all custom fields on CRM Lead

window.debugCRMLeadColumns.checkOrderSourceField()
  - Check if order_source field exists

window.debugCRMLeadColumns.manuallyFilterColumns()
  - Manually trigger column filtering

window.debugCRMLeadColumns.help()
  - Show this help message
            `);
        }
    };
    
    console.log('[CRM Lead Debug] Debug functions available at window.debugCRMLeadColumns');
    
})();
