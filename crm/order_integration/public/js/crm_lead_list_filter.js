// CRM Lead List Filter - Debug Version
// Comprehensive logging to find the issue

(function() {
    const DEBUG = true;
    let styleElement = null;
    
    function log(msg, data) {
        if (DEBUG) {
            console.log('[CRM Lead Filter] ' + msg, data || '');
        }
    }
    
    function initializeColumnFilter() {
        log('Initializing column filter...');
        
        if (typeof frappe === 'undefined' || !frappe.listview_settings) {
            log('Frappe not ready, retrying...');
            setTimeout(initializeColumnFilter, 100);
            return;
        }
        
        log('Frappe ready, setting up...');
        
        // Create style element for hiding columns
        if (!styleElement) {
            styleElement = document.createElement('style');
            styleElement.id = 'crm-lead-column-filter-style';
            document.head.appendChild(styleElement);
            log('Style element created');
        }
        
        // Set up list view settings
        frappe.listview_settings['CRM Lead'] = {
            add_fields: [
                'name',
                'first_name',
                'last_name',
                'email',
                'mobile_no',
                'status',
                'order_source',
                'assigned_to',
                'modified'
            ],
            
            get_indicator: function(doc) {
                if (doc.status === 'New') return [__('New'), 'blue', 'status,=,New'];
                if (doc.status === 'Contacted') return [__('Contacted'), 'orange', 'status,=,Contacted'];
                if (doc.status === 'Qualified') return [__('Qualified'), 'green', 'status,=,Qualified'];
                return [__(doc.status), 'gray'];
            }
        };
        
        log('List view settings configured');
        
        // Wait for list view to be ready
        setTimeout(setupListViewHooks, 2000);
    }
    
    function setupListViewHooks() {
        log('Setting up list view hooks...');
        
        if (typeof cur_list === 'undefined' || !cur_list) {
            log('cur_list not ready, retrying...');
            setTimeout(setupListViewHooks, 500);
            return;
        }
        
        log('cur_list ready, doctype:', cur_list.doctype);
        
        if (cur_list.doctype !== 'CRM Lead') {
            log('Not CRM Lead list, skipping');
            return;
        }
        
        // Hook into the refresh method
        const originalRefresh = cur_list.refresh;
        cur_list.refresh = function() {
            log('List refresh called');
            originalRefresh.call(this);
            setTimeout(filterColumns, 800);
        };
        
        log('Hooks set up, calling initial filter');
        
        // Initial filter
        filterColumns();
    }
    
    function filterColumns() {
        try {
            log('filterColumns called');
            
            if (typeof cur_list === 'undefined' || !cur_list) {
                log('cur_list not available');
                return;
            }
            
            // Get the selected Order Source from filters
            const filters = cur_list.filter_area?.get() || [];
            log('Current filters:', filters);
            
            const orderSourceFilter = filters.find(f => f[1] === 'order_source');
            const selectedOrderSource = orderSourceFilter ? orderSourceFilter[2] : null;
            
            log('Selected Order Source:', selectedOrderSource);
            
            // Get all custom fields that start with api_col_
            const fieldElements = document.querySelectorAll('[data-field^="api_col_"]');
            log('Found API column elements:', fieldElements.length);
            
            const allApiFields = [];
            fieldElements.forEach(el => {
                const fieldName = el.getAttribute('data-field');
                if (fieldName) {
                    allApiFields.push(fieldName);
                    log('Found API field:', fieldName);
                }
            });
            
            // Build CSS to hide/show columns
            let css = '';
            
            if (!selectedOrderSource) {
                log('No Order Source selected - hiding all API columns');
                allApiFields.forEach(fieldName => {
                    css += `[data-field="${fieldName}"] { display: none !important; }\n`;
                });
            } else {
                log('Order Source selected:', selectedOrderSource);
                allApiFields.forEach(fieldName => {
                    // Extract source name from field name
                    // Format: api_col_{source_name}_{column_name}
                    const parts = fieldName.split('_');
                    log('Field parts:', parts);
                    
                    if (parts.length >= 4) {
                        const sourceNameParts = parts.slice(2, -1);
                        const fieldSourceName = sourceNameParts.join('_');
                        const selectedSourceNormalized = selectedOrderSource.toLowerCase().replace(/-/g, '_');
                        
                        log('Field source:', fieldSourceName, 'Selected source:', selectedSourceNormalized);
                        
                        if (fieldSourceName === selectedSourceNormalized) {
                            log('SHOWING column:', fieldName);
                            css += `[data-field="${fieldName}"] { display: table-cell !important; visibility: visible !important; }\n`;
                        } else {
                            log('HIDING column:', fieldName);
                            css += `[data-field="${fieldName}"] { display: none !important; }\n`;
                        }
                    }
                });
            }
            
            log('CSS to apply:', css);
            
            // Apply CSS
            if (styleElement) {
                styleElement.textContent = css;
                log('CSS applied to style element');
            }
            
        } catch (e) {
            console.error('[CRM Lead Filter] Error filtering columns:', e);
        }
    }
    
    // Start initialization
    log('Script loaded, starting initialization');
    initializeColumnFilter();
    
    // Also watch for manual filter changes
    $(document).on('click', '[data-order-source-filter="true"] [data-source-value]', function() {
        log('Order Source filter clicked');
        setTimeout(filterColumns, 500);
    });
    
    // Watch for filter area changes
    $(document).on('change', '.filter-area', function() {
        log('Filter area changed');
        setTimeout(filterColumns, 500);
    });
    
    // Expose filterColumns globally for manual testing
    window.debugFilterColumns = filterColumns;
    log('Debug function exposed as window.debugFilterColumns()');
    
})();
