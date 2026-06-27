# System Architecture - Column Filtering

## High-Level Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERACTION                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. User syncs API source                                       │
│     └─> Order Sync Sources → Select Source → Click "Sync Now"  │
│                                                                 │
│  2. System detects columns from API response                    │
│     └─> DynamicLeadIngestion.extract_displayable_fields()      │
│                                                                 │
│  3. Custom fields are created on CRM Lead                       │
│     └─> api_col_{source_name}_{column_name}                    │
│                                                                 │
│  4. Leads are created with API data                             │
│     └─> populate_custom_fields_for_lead()                      │
│                                                                 │
│  5. User goes to CRM Lead list view                             │
│     └─> /app/crm-lead                                          │
│                                                                 │
│  6. User adds Order Source filter                               │
│     └─> Filter icon → Add Filter → Order Source → Apply        │
│                                                                 │
│  7. Columns are instantly filtered                              │
│     └─> crm_lead_column_manager.js detects filter change       │
│     └─> CSS is applied to show/hide columns                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow - Column Creation

```
┌──────────────────┐
│  External API    │
│  (e.g., Shopify) │
└────────┬─────────┘
         │
         │ HTTP Request with Bearer Token
         │
         ▼
┌──────────────────────────────────────┐
│  _fetch_orders_from_api()            │
│  - Tries multiple auth formats       │
│  - Returns JSON array                │
└────────┬─────────────────────────────┘
         │
         │ List of order objects
         │
         ▼
┌──────────────────────────────────────┐
│  DynamicLeadIngestion.detect_schema()│
│  - Analyzes first record             │
│  - Detects field types               │
└────────┬─────────────────────────────┘
         │
         │ Schema: {field: type}
         │
         ▼
┌──────────────────────────────────────┐
│  extract_displayable_fields()        │
│  - Prioritizes important fields      │
│  - Returns top 15 fields             │
└────────┬─────────────────────────────┘
         │
         │ List of column names
         │
         ▼
┌──────────────────────────────────────┐
│  save_api_schema()                   │
│  - Stores in API Schema Storage      │
│  - Stores metadata                   │
└────────┬─────────────────────────────┘
         │
         │ Schema saved
         │
         ▼
┌──────────────────────────────────────┐
│  create_custom_fields_for_columns()  │
│  - Creates field for each column     │
│  - Sets description: api_source:...  │
│  - Sets read_only: 1                 │
└────────┬─────────────────────────────┘
         │
         │ Custom fields created
         │
         ▼
┌──────────────────────────────────────┐
│  _create_lead_from_order()           │
│  - Creates CRM Lead                  │
│  - Sets order_source field           │
└────────┬─────────────────────────────┘
         │
         │ Lead created
         │
         ▼
┌──────────────────────────────────────┐
│  populate_custom_fields_for_lead()   │
│  - Gets schema for source            │
│  - Populates each custom field       │
│  - Handles nested fields             │
└────────┬─────────────────────────────┘
         │
         │ Lead with API data
         │
         ▼
┌──────────────────────────────────────┐
│  CRM Lead with API Columns           │
│  - lead_name: "John Doe"             │
│  - email: "john@example.com"         │
│  - api_col_source_name_field1: "..." │
│  - api_col_source_name_field2: "..." │
└──────────────────────────────────────┘
```

---

## Data Flow - Column Filtering

```
┌──────────────────────────────────────┐
│  CRM Lead List View Loaded           │
│  - boot.py injects scripts           │
│  - crm_lead_column_manager.js runs   │
└────────┬─────────────────────────────┘
         │
         │ Script initialization
         │
         ▼
┌──────────────────────────────────────┐
│  loadApiColumns()                    │
│  - Queries Custom Field table        │
│  - Filters: fieldname LIKE api_col_% │
│  - Extracts source from description  │
└────────┬─────────────────────────────┘
         │
         │ sourceColumnMap = {
         │   "source1": ["col1", "col2"],
         │   "source2": ["col3", "col4"]
         │ }
         │
         ▼
┌──────────────────────────────────────┐
│  setupListView()                     │
│  - Waits for cur_list to be ready    │
│  - Hooks into filter changes         │
│  - Hooks into refresh                │
└────────┬─────────────────────────────┘
         │
         │ Hooks installed
         │
         ▼
┌──────────────────────────────────────┐
│  User selects Order Source filter    │
│  - Filter area detects change        │
│  - updateVisibility() is called      │
└────────┬─────────────────────────────┘
         │
         │ Filter change detected
         │
         ▼
┌──────────────────────────────────────┐
│  updateVisibility()                  │
│  - Gets current filters              │
│  - Finds order_source filter value   │
│  - Looks up columns for that source  │
└────────┬─────────────────────────────┘
         │
         │ columnsToShow = ["col1", "col2"]
         │
         ▼
┌──────────────────────────────────────┐
│  updateColumnCSS()                   │
│  - Creates style element             │
│  - Hides all API columns             │
│  - Shows selected source columns     │
└────────┬─────────────────────────────┘
         │
         │ CSS applied:
         │ [data-field="api_col_..."] {
         │   display: none !important;
         │ }
         │ [data-field="api_col_source1_..."] {
         │   display: table-cell !important;
         │ }
         │
         ▼
┌──────────────────────────────────────┐
│  Browser Renders Updated List        │
│  - API columns from selected source  │
│    are visible                       │
│  - API columns from other sources    │
│    are hidden                        │
│  - Default columns always visible    │
└──────────────────────────────────────┘
```

---

## Database Schema

### Custom Field (for API columns)

```
Custom Field
├── name: "CRM Lead-api_col_source_name_column"
├── dt: "CRM Lead"
├── fieldname: "api_col_source_name_column"
├── fieldtype: "Data"
├── label: "Source Name: Column"
├── description: "api_source:source_name"  ← Metadata
├── in_list_view: 0
├── read_only: 1
└── ...
```

### Custom Field (for Order Source filter)

```
Custom Field
├── name: "CRM Lead-order_source"
├── dt: "CRM Lead"
├── fieldname: "order_source"
├── fieldtype: "Link"
├── options: "Order Sync Source"
├── in_standard_filter: 1  ← Shows in filter dropdown
└── ...
```

### CRM Lead (with API data)

```
CRM Lead
├── name: "lead_id_12345"
├── lead_name: "John Doe"
├── email: "john@example.com"
├── mobile_no: "1234567890"
├── status: "New"
├── order_source: "source_name"  ← Links to Order Sync Source
├── api_col_source_name_field1: "value1"
├── api_col_source_name_field2: "value2"
└── ...
```

### API Schema Storage

```
API Schema Storage
├── name: "source_name"
├── order_source: "source_name"
├── schema_fields: "{...}"  ← JSON with field types
├── columns: "[...]"  ← JSON array of column names
└── ...
```

---

## JavaScript Architecture

### crm_lead_column_manager.js

```
IIFE (Immediately Invoked Function Expression)
│
├─ init()
│  ├─ Create style element
│  ├─ loadApiColumns()
│  └─ setupListView()
│
├─ loadApiColumns()
│  └─ frappe.call() → Get all api_col_* fields
│     └─ Build sourceColumnMap
│
├─ setupListView()
│  ├─ Wait for cur_list
│  ├─ Hook into filter changes
│  ├─ Hook into refresh
│  └─ Call updateVisibility()
│
├─ updateVisibility()
│  ├─ Get current filters
│  ├─ Find order_source filter
│  └─ Call updateColumnCSS()
│
└─ updateColumnCSS()
   ├─ Build CSS rules
   ├─ Hide all API columns
   ├─ Show selected source columns
   └─ Apply to style element
```

### crm_lead_list_debug.js

```
window.debugCRMLeadColumns
│
├─ getAllApiColumns()
│  └─ frappe.call() → Get all api_col_* fields
│
├─ getCurrentFilters()
│  └─ Get cur_list.filter_area.get()
│
├─ getListViewColumns()
│  └─ Query DOM for column headers
│
├─ testCSSApplication()
│  └─ Apply test CSS to verify selectors work
│
├─ getAllCustomFields()
│  └─ frappe.call() → Get all custom fields
│
├─ checkOrderSourceField()
│  └─ frappe.call() → Get order_source field
│
├─ manuallyFilterColumns()
│  └─ Manually trigger filtering logic
│
└─ help()
   └─ Print all available functions
```

---

## Event Flow

```
User Action                    Script Response
─────────────────────────────────────────────────────────────

1. Page loads                  → boot.py injects scripts
                               → crm_lead_column_manager.js runs
                               → loadApiColumns() called
                               → setupListView() called

2. Filter area rendered        → updateVisibility() called
                               → CSS applied (all columns hidden)

3. User adds filter            → Filter change detected
                               → updateVisibility() called
                               → CSS updated (show selected columns)

4. User changes filter         → Filter change detected
                               → updateVisibility() called
                               → CSS updated (show new columns)

5. User removes filter         → Filter change detected
                               → updateVisibility() called
                               → CSS updated (hide all columns)

6. User refreshes list         → refresh() hook called
                               → updateVisibility() called
                               → CSS reapplied
```

---

## CSS Selectors Used

```javascript
// Hide all API columns
[data-field="api_col_..."] { display: none !important; }
[data-fieldname="api_col_..."] { display: none !important; }
.list-row-col[data-field="api_col_..."] { display: none !important; }
.list-row-col[data-fieldname="api_col_..."] { display: none !important; }

// Show selected source columns
[data-field="api_col_source_..."] { display: table-cell !important; }
[data-fieldname="api_col_source_..."] { display: table-cell !important; }
.list-row-col[data-field="api_col_source_..."] { display: table-cell !important; }
.list-row-col[data-fieldname="api_col_source_..."] { display: table-cell !important; }
```

---

## Error Handling

```
Try to load API columns
├─ Success → Build sourceColumnMap
└─ Error → Log error, continue

Try to setup list view
├─ Success → Install hooks
└─ Error → Retry after 500ms

Try to update visibility
├─ Success → Apply CSS
└─ Error → Log error, continue

Try to apply CSS
├─ Success → Columns update
└─ Error → Log error, continue
```

---

## Performance Optimization

1. **Lazy Loading** - Debug functions only load when called
2. **CSS-based Hiding** - No DOM manipulation, just CSS
3. **Event Debouncing** - Updates only when filter actually changes
4. **Caching** - sourceColumnMap cached in memory
5. **Minimal Queries** - Only queries database once on page load

---

## Browser Compatibility

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| CSS display property | ✅ | ✅ | ✅ | ✅ |
| data-* attributes | ✅ | ✅ | ✅ | ✅ |
| querySelector | ✅ | ✅ | ✅ | ✅ |
| frappe.call() | ✅ | ✅ | ✅ | ✅ |
| setTimeout | ✅ | ✅ | ✅ | ✅ |
| IIFE | ✅ | ✅ | ✅ | ✅ |

---

## Troubleshooting Decision Tree

```
Columns not showing/hiding?
│
├─ Order Source field exists?
│  ├─ No → Run setup_order_source_filter()
│  └─ Yes → Continue
│
├─ API columns created?
│  ├─ No → Sync an API source
│  └─ Yes → Continue
│
├─ Filter applied?
│  ├─ No → Add Order Source filter
│  └─ Yes → Continue
│
├─ CSS being applied?
│  ├─ No → Check DevTools for style element
│  └─ Yes → Continue
│
├─ CSS selectors matching?
│  ├─ No → Inspect DOM to find correct selectors
│  └─ Yes → Continue
│
└─ Check browser console for errors
   ├─ Errors found → Fix errors
   └─ No errors → System working correctly
```

