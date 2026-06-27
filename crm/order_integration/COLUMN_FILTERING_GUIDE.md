# Column Filtering - Testing & Debugging Guide

## Overview

The column filtering system automatically shows/hides API columns based on the selected Order Source filter in the CRM Lead list view.

**How it works:**
1. When you sync orders from an API, custom fields are created with names like `api_col_{source_name}_{column_name}`
2. The source name is stored in the field's description as `api_source:{source_name}`
3. When you select an Order Source filter, only columns from that source are shown
4. When no filter is selected, all API columns are hidden

---

## Step 1: Verify Setup

### Check if Order Source field exists

Open browser console (F12) and run:

```javascript
window.debugCRMLeadColumns.checkOrderSourceField()
```

**Expected output:** Should show a Custom Field document with:
- `fieldname: "order_source"`
- `fieldtype: "Link"`
- `options: "Order Sync Source"`
- `in_standard_filter: 1`

**If NOT found:** Run this in the Frappe console:
```bash
bench --site <your-site> console
```

Then in Python:
```python
from order_integration.order_integration.api.setup_order_source_field import setup_order_source_filter
setup_order_source_filter()
```

---

## Step 2: Verify API Columns are Created

### Get all API columns

Open browser console and run:

```javascript
window.debugCRMLeadColumns.getAllApiColumns()
```

**Expected output:** Should show a table with columns like:
- `api_col_source_name_column_name`
- `api_col_source_name_another_column`
- etc.

**If NO columns found:**
1. Make sure you've synced at least one API source
2. Go to Order Sync Sources and click "Sync Now"
3. Check the sync result - should show "leads created"
4. Then run the debug command again

---

## Step 3: Verify Leads Have Data

### Check if leads were created with API data

Go to CRM Lead list view and:
1. Click "Add Column" dropdown
2. Look for columns starting with `api_col_`
3. If you see them, manually add one to the view
4. Check if the lead has data in that column

**If columns don't appear in "Add Column" dropdown:**
- The custom fields weren't created properly
- Re-run the sync: Go to Order Sync Sources → Click "Sync Now"

---

## Step 4: Test the Filter

### Add Order Source filter manually

1. Go to CRM Lead list view
2. Click the filter icon (funnel icon)
3. Click "Add Filter"
4. Select "Order Source" from the dropdown
5. Select an Order Source that has synced data
6. Click "Apply"

**Expected behavior:**
- API columns from that source should become visible
- API columns from other sources should be hidden
- Default columns (Name, Email, Status, etc.) should always be visible

**If columns don't show/hide:**
- Continue to Step 5 for debugging

---

## Step 5: Debug the Filtering Logic

### Check current filter state

```javascript
window.debugCRMLeadColumns.getCurrentFilters()
```

**Expected output:** Should show an array with the Order Source filter:
```
[
  ["CRM Lead", "order_source", "=", "your-source-name"]
]
```

### Check list view columns

```javascript
window.debugCRMLeadColumns.getListViewColumns()
```

**Expected output:** Should show:
- `Fields:` array with column names
- `DOM Column Headers:` count of visible columns
- List of columns with their `data-field` and `data-fieldname` attributes

### Test CSS application

```javascript
window.debugCRMLeadColumns.testCSSApplication()
```

**Expected behavior:**
- A test style is applied
- If you see any columns turn red, the CSS selectors are working
- If NO columns turn red, the DOM selectors don't match the actual structure

---

## Step 6: Manually Trigger Filtering

### Force column filtering

```javascript
window.debugCRMLeadColumns.manuallyFilterColumns()
```

**What this does:**
1. Gets the current Order Source filter value
2. Loads all API columns from database
3. Maps columns to their source
4. Applies CSS to show/hide columns
5. Logs the result to console

**Check the console output:**
- `Selected Order Source:` should show your selected source
- `Source Column Map:` should show which columns belong to each source
- `Columns to show:` should list the columns that will be visible
- `CSS applied.` message should appear

**If columns still don't show/hide:**
- The CSS selectors might not match the DOM structure
- Continue to Step 7

---

## Step 7: Inspect the DOM

### Check column header structure

Open browser DevTools (F12) → Elements tab

1. Find a column header in the table
2. Right-click → Inspect
3. Look at the HTML structure

**Expected structure:**
```html
<div class="list-row-col" data-field="api_col_source_name_column" data-fieldname="api_col_source_name_column">
  Column Header Text
</div>
```

**Check the attributes:**
- Does it have `data-field` attribute?
- Does it have `data-fieldname` attribute?
- What are the exact values?

### Check if CSS is being applied

1. In DevTools, go to Elements tab
2. Find the `<style id="crm-lead-api-column-filter">` element
3. Check if it contains CSS rules
4. Check if the CSS selectors match the column elements

**If CSS is not in the style element:**
- The script is not running
- Check browser console for errors
- Refresh the page and try again

---

## Step 8: Common Issues & Solutions

### Issue: "Order Source filter doesn't appear in filter dropdown"

**Solution:**
1. The `order_source` field might not be created
2. Run setup again:
   ```bash
   bench --site <your-site> console
   ```
   ```python
   from order_integration.order_integration.api.setup_order_source_field import setup_order_source_filter
   setup_order_source_filter()
   ```
3. Refresh the page

### Issue: "API columns don't appear in 'Add Column' dropdown"

**Solution:**
1. Sync an API source first
2. Go to Order Sync Sources → Select a source → Click "Sync Now"
3. Wait for sync to complete
4. Go back to CRM Lead list
5. Click "Add Column" - the new columns should appear

### Issue: "Columns show/hide but not correctly"

**Solution:**
1. Run the debug commands to check:
   - `window.debugCRMLeadColumns.getCurrentFilters()`
   - `window.debugCRMLeadColumns.manuallyFilterColumns()`
2. Check the console output for errors
3. If CSS is not being applied, check the DOM structure with DevTools

### Issue: "Script errors in console"

**Solution:**
1. Check the error message
2. If it says "frappe is not defined", the page hasn't loaded yet
3. Wait a few seconds and try again
4. If it persists, refresh the page

---

## Step 9: Production Verification

### Final checklist

- [ ] Order Source field exists on CRM Lead
- [ ] API columns are created after sync
- [ ] Leads have data in API columns
- [ ] Order Source filter appears in filter dropdown
- [ ] Selecting Order Source filter shows/hides columns correctly
- [ ] No errors in browser console
- [ ] Works on multiple Order Sources

### If all checks pass:

The column filtering system is working correctly! Users can now:
1. Sync orders from an API
2. Columns are automatically created
3. Select Order Source filter to see only that source's columns
4. No manual column selection needed

---

## Advanced Debugging

### Get all custom fields on CRM Lead

```javascript
window.debugCRMLeadColumns.getAllCustomFields()
```

This shows all custom fields, not just API columns. Useful for checking if fields are being created at all.

### Check browser console for errors

1. Open DevTools (F12)
2. Go to Console tab
3. Look for any red error messages
4. Copy the error and search for it in the code

### Check server logs

```bash
bench --site <your-site> tail -f
```

Look for any errors related to:
- "Order Sync Error"
- "API Schema Storage"
- "Order Integration"

---

## Contact Support

If you've gone through all these steps and the filtering still doesn't work:

1. Run all debug commands and save the console output
2. Check the server logs for errors
3. Provide:
   - Browser console output
   - Server logs
   - Steps to reproduce
   - Expected vs actual behavior

