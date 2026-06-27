// CRM Lead Column Manager - Production Ready
// Manages API column visibility based on Order Source filter

(function() {
    let sourceColumnMap = {};
    let allApiColumns = [];
    let currentSelectedSource = null;
    let styleElement = null;
    
    function init() {
        if (typeof frappe === 'undefined') {
            setTimeout(init, 100);
            return;
        }
        
        // Create style element
        styleElement = document.createElement('style');
        styleElement.id = 'crm-lead-api-column-filter';
        document.head.appendChild(styleElement);
        
        // Load all API columns from database
        loadApiColumns();
        
        // Wait for list view
        setTimeout(setupListView, 2000);
    }
    
    function loadApiColumns() {
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
                if (r.message) {
                    r.message.forEach(cf => {
                        allApiColumns.push(cf.fieldname);
                        
                        // Extract source from description
                        if (cf.description && cf.description.includes('api_source:')) {
                            const source = cf.description.split('api_source:')[1].trim();
                            if (!sourceColumnMap[source]) {
                                sourceColumnMap[source] = [];
                            }
                            sourceColumnMap[source].push(cf.fieldname);
                        }
                    });
                }
            }
        });
    }
    
    function setupListView() {
        if (typeof cur_list === 'undefined' || !cur_list || cur_list.doctype !== 'CRM Lead') {
            setTimeout(setupListView, 500);
            return;
        }
        
        // Watch for filter changes using jQuery event delegation
        $(document).on('change', '.filter-area', function() {
            setTimeout(updateVisibility, 300);
        });
        
        // Also watch for filter button clicks
        $(document).on('click', '.filter-menu-button, .filter-button', function() {
            setTimeout(updateVisibility, 500);
        });
        
        // Hook into refresh
        const originalRefresh = cur_list.refresh;
        cur_list.refresh = function() {
            const result = originalRefresh.call(this);
            setTimeout(updateVisibility, 800);
            return result;
        };
        
        // Initial update
        updateVisibility();
    }
    
    function updateVisibility() {
        try {
            if (typeof cur_list === 'undefined' || !cur_list) {
                return;
            }
            
            // Get current filter value
            const filters = cur_list.filter_area?.get() || [];
            const orderSourceFilter = filters.find(f => f[1] === 'order_source');
            const selectedSource = orderSourceFilter ? orderSourceFilter[2] : null;
            
            // Only update if source changed
            if (selectedSource === currentSelectedSource) {
                return;
            }
            
            currentSelectedSource = selectedSource;
            
            // Determine which columns to show
            const columnsToShow = selectedSource ? (sourceColumnMap[selectedSource] || []) : [];
            
            // Update column visibility using CSS
            updateColumnCSS(columnsToShow);
            
        } catch (e) {
            console.error('[CRM Lead Column Manager] Error updating visibility:', e);
        }
    }
    
    function updateColumnCSS(columnsToShow) {
        if (!styleElement) {
            return;
        }
        
        let css = '';
        
        // Hide all API columns
        allApiColumns.forEach(colName => {
            // Multiple selectors to ensure we catch all variations
            css += `[data-field="${colName}"] { display: none !important; }\n`;
            css += `[data-fieldname="${colName}"] { display: none !important; }\n`;
            css += `.list-row-col[data-field="${colName}"] { display: none !important; }\n`;
            css += `.list-row-col[data-fieldname="${colName}"] { display: none !important; }\n`;
        });
        
        // Show only selected source's columns
        columnsToShow.forEach(colName => {
            css += `[data-field="${colName}"] { display: table-cell !important; }\n`;
            css += `[data-fieldname="${colName}"] { display: table-cell !important; }\n`;
            css += `.list-row-col[data-field="${colName}"] { display: table-cell !important; }\n`;
            css += `.list-row-col[data-fieldname="${colName}"] { display: table-cell !important; }\n`;
        });
        
        styleElement.textContent = css;
    }
    
    // Start
    init();
    
})();
