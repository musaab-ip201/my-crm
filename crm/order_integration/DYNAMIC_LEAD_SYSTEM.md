# Dynamic Lead Ingestion & Visualization System

## Overview

This system enables flexible ingestion of data from external APIs with automatic schema detection, field mapping, and dynamic table generation. No fixed schema required - adapts to any API response structure.

## Core Components

### 1. API Source Configuration (`Order Sync Source`)

**Fields:**
- `source_name`: Display name for the source
- `source_type`: Type of source (e.g., ipshopy.com, Shop.com)
- `api_url`: Full URL to the API endpoint
- `access_token`: Bearer token for authentication
- `sync_frequency`: Background sync interval (5 min, 10 min, hourly, daily)
- `last_synced_at`: Timestamp of last sync

**Features:**
- Multiple sources can be configured
- Each source is independent
- Bearer token authentication with retry logic (3 attempts, exponential backoff)
- SSL verification enabled for production

### 2. Dynamic Schema Detection (`dynamic_lead_api.py`)

**Auto-Detection Features:**

#### Schema Detection
```python
detect_schema(api_response) -> Dict[str, str]
```
Analyzes API response and returns field types:
- `string`: Text fields
- `number`: Numeric fields
- `boolean`: Boolean fields
- `object`: Nested objects
- `array`: Array fields

#### Field Auto-Mapping
```python
auto_map_fields(api_response) -> Dict[str, str]
```

Maps API fields to CRM Lead fields using priority-based matching:

**Name Fields Priority:**
1. `name`
2. `customer_name`
3. `customer`
4. `full_name`
5. `title`

**Email Fields Priority:**
1. `email`
2. `customer_email`
3. `email_address`

**Phone Fields Priority:**
1. `phone`
2. `mobile`
3. `mobile_no`
4. `telephone`
5. `contact_number`

**Status Fields Priority:**
1. `status`
2. `order_status`
3. `state`
4. `stage`

**ID Fields Priority:**
1. `id`
2. `order_id`
3. `cart_id`
4. `customer_id`
5. `reference_id`

#### Displayable Fields Extraction
```python
extract_displayable_fields(api_response, max_fields=10) -> List[str]
```

Intelligently selects up to 10 most relevant fields for table display:
1. ID fields (order_id, cart_id, customer_id)
2. Name fields
3. Email fields
4. Phone fields
5. Status fields
6. Date fields
7. Other fields

### 3. API Response Parsing

**Supported Response Formats:**

```json
// Format 1: Direct array
[
  { "id": 1, "name": "John", "email": "john@example.com" },
  { "id": 2, "name": "Jane", "email": "jane@example.com" }
]

// Format 2: Wrapped in 'data' key
{
  "data": [
    { "id": 1, "name": "John" },
    { "id": 2, "name": "Jane" }
  ]
}

// Format 3: Wrapped in 'records' key
{
  "records": [
    { "id": 1, "name": "John" },
    { "id": 2, "name": "Jane" }
  ]
}

// Format 4: Paginated response
{
  "data": [...],
  "total": 100,
  "total_pages": 5,
  "current_page": 1
}
```

### 4. Dynamic Lead Creation

**Lead Mapping Logic:**

```python
create_leads_from_api_data(
    source_name: str,
    records: List[Dict],
    field_mapping: Dict
) -> Dict
```

**Validation:**
- At least email OR phone required
- Duplicate detection by email/phone
- Phone normalization (strips non-digits)
- Status validation against CRM Lead Status values

**Created Fields:**
- `lead_name`: From mapped name field
- `email`: From mapped email field
- `mobile_no`: From mapped phone field
- `status`: From mapped status field (defaults to "New")
- `order_status`: Same as status
- `order_id`: From mapped ID field

**Error Handling:**
- Tracks failed records with reasons
- Returns summary: created count, failed count, details

### 5. Dynamic Lead Viewer UI (`DynamicLeadViewer.vue`)

**Features:**

#### Source Selection
- Dropdown with all configured API sources
- Auto-loads source list on component mount

#### Data Loading
- Fetches data from selected API source
- Displays loading state during fetch
- Shows error messages if fetch fails

#### Schema Display
- Shows detected field types as badges
- Color-coded by type (blue theme)

#### Field Mapping Display
- Shows auto-detected CRM ← API field mappings
- Helps users understand data transformation

#### Dynamic Table
- Columns generated from `displayable_fields`
- Shows up to 10 most relevant fields
- Truncates long values (100 chars max)
- Hover effect on rows

#### Individual Lead Creation
- "Create Lead" button for each row
- Validates before creation
- Shows success/error toast
- Removes row after successful creation

#### Pagination
- Shows current page and total records
- Previous/Next buttons
- Disabled when at boundaries
- Page size: 20 records per page

### 6. API Endpoints

#### `fetch_api_data`
```python
@frappe.whitelist()
def fetch_api_data(source_name: str, page: int = 1, page_size: int = 20) -> Dict
```

**Returns:**
```json
{
  "status": "success",
  "records": [...],
  "schema": { "field": "type", ... },
  "field_mapping": { "crm_field": "api_field", ... },
  "displayable_fields": ["field1", "field2", ...],
  "is_paginated": true,
  "total_records": 100,
  "page": 1,
  "page_size": 20
}
```

#### `get_api_sources_for_filter`
```python
@frappe.whitelist()
def get_api_sources_for_filter() -> List[Dict]
```

**Returns:**
```json
[
  { "name": "source1", "source_name": "My Store", "source_type": "ipshopy.com" },
  { "name": "source2", "source_name": "Another Store", "source_type": "Shop.com" }
]
```

#### `create_leads_from_api_data`
```python
@frappe.whitelist()
def create_leads_from_api_data(
    source_name: str,
    records: List[Dict],
    field_mapping: Dict
) -> Dict
```

**Returns:**
```json
{
  "status": "success",
  "created": 5,
  "failed": 2,
  "created_leads": [
    { "name": "lead1", "lead_name": "John", "email": "john@example.com" }
  ],
  "failed_records": [
    { "index": 0, "reason": "No email or phone provided" }
  ]
}
```

## Usage Flow

### 1. Configure API Source
1. Go to CRM Settings → Order Syncing
2. Click "New"
3. Fill in:
   - Source Name: "My Store"
   - Source Type: "ipshopy.com"
   - API URL: "https://api.mystore.com/orders"
   - Access Token: "your_bearer_token"
   - Sync Frequency: "Every 5 Minutes"
4. Click "Test Connection" to verify
5. Click "Create"

### 2. View Dynamic Data
1. In Order Syncing settings, click "Dynamic Lead Viewer" tab
2. Select source from dropdown
3. Click "Load Data"
4. System automatically:
   - Fetches data from API
   - Detects schema
   - Maps fields
   - Displays table with relevant columns

### 3. Create Leads
1. Review data in dynamic table
2. Click "Create Lead" for individual records
3. Or select multiple and bulk create
4. System validates and creates leads
5. Shows success/error for each record

## Scalability Features

### Pagination Support
- API responses with `total_pages` detected as paginated
- Previous/Next navigation
- Configurable page size (default: 20)
- Lazy loading on demand

### Performance Optimizations
- Limits displayable fields to 10 (configurable)
- Truncates long values (100 chars)
- Efficient schema detection (samples first record)
- Batch lead creation support

### Error Handling
- Retry logic for API calls (3 attempts, exponential backoff)
- Detailed error messages for failed records
- Graceful degradation if API unavailable
- Comprehensive logging

## Example API Responses

### Example 1: E-commerce Orders
```json
[
  {
    "order_id": "ORD-001",
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "customer_phone": "+1-555-0123",
    "order_status": "Placed",
    "order_date": "2026-04-26",
    "total_amount": 299.99
  }
]
```

**Auto-Detected Mapping:**
- `lead_name` ← `customer_name`
- `email` ← `customer_email`
- `mobile_no` ← `customer_phone`
- `order_status` ← `order_status`
- `order_id` ← `order_id`

**Displayable Fields:**
- order_id, customer_name, customer_email, customer_phone, order_status, order_date, total_amount

### Example 2: Cart Abandonment
```json
{
  "data": [
    {
      "cart_id": "CART-123",
      "name": "Jane Smith",
      "email": "jane@example.com",
      "phone": "555-0456",
      "status": "Added to Cart",
      "items_count": 3,
      "cart_value": 150.00
    }
  ]
}
```

**Auto-Detected Mapping:**
- `lead_name` ← `name`
- `email` ← `email`
- `mobile_no` ← `phone`
- `order_status` ← `status`
- `order_id` ← `cart_id`

### Example 3: Paginated Response
```json
{
  "records": [...],
  "total": 500,
  "total_pages": 25,
  "current_page": 1,
  "per_page": 20
}
```

**Pagination Detected:** Yes
- Shows page navigation
- Fetches next page on demand

## Configuration

### Field Mapping Customization (Future)
Currently auto-detected. Future enhancement to allow manual mapping:

```python
# Custom mapping example
custom_mapping = {
    "lead_name": "full_name",
    "email": "contact_email",
    "mobile_no": "phone_number",
    "order_status": "order_state"
}
```

### Displayable Fields Customization (Future)
```python
# Custom field selection
displayable_fields = [
    "order_id",
    "customer_name",
    "email",
    "status",
    "created_at"
]
```

## Troubleshooting

### API Connection Failed
- Verify API URL is correct
- Check Bearer token is valid
- Ensure SSL certificate is valid (or disable for dev)
- Check network connectivity

### No Data Loaded
- Verify API returns valid JSON
- Check response format is supported
- Ensure API returns array or wrapped in known key
- Check API authentication

### Field Mapping Incorrect
- Review auto-detected mapping in UI
- Check API response field names
- Verify field names match priority list
- Consider custom mapping (future feature)

### Duplicate Leads Created
- System checks email and phone for duplicates
- Ensure API data doesn't have duplicates
- Check CRM Lead database for existing records

## Future Enhancements

1. **Custom Field Mapping UI**
   - Drag-and-drop field mapping
   - Save mapping templates
   - Reuse mappings across sources

2. **Advanced Filtering**
   - Filter records before creating leads
   - Conditional lead creation rules
   - Data transformation pipelines

3. **Bulk Operations**
   - Select multiple records
   - Bulk create leads
   - Bulk update existing leads

4. **Data Validation**
   - Custom validation rules
   - Data quality checks
   - Duplicate detection strategies

5. **Webhook Support**
   - Real-time data ingestion
   - Event-driven lead creation
   - Bi-directional sync

6. **Analytics**
   - Sync history and statistics
   - Success/failure rates
   - Performance metrics
   - Data quality reports
