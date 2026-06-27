Dynamic JSON Column Injection Plan
This plan details how to modify the system so that when a user adds any API in the Order Syncing settings, the system automatically parses the API's JSON response and injects those dynamic fields as columns into both the Lead List view and the Lead Details page.

1. Remove Hardcoded Data Type Configurations
Currently, the system is hardcoded to only accept cart_data and ticket_data via dictionaries like COLUMN_CONFIG and DATA_TYPE_CONFIG.

lead_list_dynamic_columns_api.py & lead_source_data_api.py
[MODIFY]: Remove the hardcoded COLUMN_CONFIG and DATA_TYPE_CONFIG dictionaries.
[MODIFY]: Instead of fetching config by data_type, query the Order Sync Source directly using the source_name.
[MODIFY]: Use the target source's api_url directly.
[MODIFY]: Use the flatten_dict utility on the first fetched record to dynamically extract all JSON keys (e.g., {"order_id": 1, "custom_field": "x"}). Create column definitions dynamically where the label is formatted nicely (e.g., "Custom Field").
2. Lead List View Injection
The Lead List view uses an override on the standard API and a frontend script.

override_get_data.py
[MODIFY]: Remove logic that restricts injection to keys found in COLUMN_CONFIG.
[MODIFY]: Extract source_name from the list view filters. Fetch the dynamic columns directly from get_dynamic_columns_data and inject them dynamically into the columns array.
public/js/crm_lead_list.js (Filter Event Listener)
[MODIFY]: Ensure the script actively listens to the Order Source filter selection. When the user selects an API source (e.g., "cart data", "ticket data", or a custom API) from the filter dropdown, the script must automatically trigger and pass the selected order_source to the backend.
[MODIFY]: The backend will return the dynamic columns for that specific API, and the script will inject them into listview.columns, replacing the default columns for that specific view.
[MODIFY]: If the user clears the Order Source filter, automatically reset the list view to the standard columns.
3. Lead Details Page Injection
When a user opens a specific Lead, they should see the custom JSON data.

Frontend UI (Vue / order_sync_components.js)
[MODIFY]: Ensure the table or data panel in the Lead Details page loops through the dynamic columns array returned by get_lead_source_data. Instead of hardcoding <tr><th>Product</th>...</tr>, use v-for="col in columns" to render headers, and v-for="row in records" to render the cell values.
4. Settings Form Improvements
order_sync_source.py
[MODIFY]: Remove the _auto_set_source_type method that forces the source to either be "cart_data" or "ticket_data".
[MODIFY]: Allow source_type to be auto-generated based on the user-provided "Source Name" (e.g., converting "My Custom API" to my_custom_api) or simply rely entirely on source_name as the unique identifier.
Verification Plan
Manual Verification
Create generic API source: Go to Order Sync settings, add an API that returns completely different fields (e.g., {"warranty_status": "Active", "serial_no": "XYZ"}).
Lead List: Navigate to the Lead List, filter by the new source, and verify that "Warranty Status" and "Serial No" appear as columns populated with data.
Lead Details: Click into a Lead. Verify that the dynamic details section displays the new JSON fields correctly for that lead.
