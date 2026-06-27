# Testing Checklist - Column Filtering

## Pre-Testing Setup

- [ ] Frappe bench is running
- [ ] Order Integration app is installed
- [ ] At least one Order Sync Source is configured
- [ ] Browser console is accessible (F12)

---

## Phase 1: Verify Setup (5 minutes)

### 1.1 Check Order Source Field
```javascript
window.debugCRMLeadColumns.checkOrderSourceField()
```
- [ ] Command runs without errors
- [ ] Shows Custom Field document
- [ ] fieldname is "order_source"
- [ ] fieldtype is "Link"
- [ ] options is "Order Sync Source"
- [ ] in_standard_filter is 1

**If failed:** Run setup in Frappe console:
```python
from order_integration.order_integration.api.setup_order_source_field import setup_order_source_filter
setup_order_source_filter()
```

### 1.2 Check API Columns
```javascript
window.debugCRMLeadColumns.getAllApiColumns()
```
- [ ] Command runs without errors
- [ ] Shows table of API columns (if data synced)
- [ ] Column names start with "api_col_"
- [ ] Description contains "api_source:"

**If no columns:** Sync an API source first

---

## Phase 2: Sync API Data (5 minutes)

### 2.1 Sync an Order Source
1. [ ] Go to Order Sync Sources
2. [ ] Select a source
3. [ ] Click "Sync Now"
4. [ ] Wait for completion
5. [ ] Check result shows "leads created"

### 2.2 Verify Leads Created
1. [ ] Go to CRM Lead list
2. [ ] Check if new leads appear
3. [ ] Click on a lead
4. [ ] Check if it has data in custom fields

### 2.3 Verify Custom Fields Created
```javascript
window.debugCRMLeadColumns.getAllApiColumns()
```
- [ ] Command shows API columns
- [ ] Column count matches API response fields
- [ ] All columns have "api_source:" in description

---

## Phase 3: Test Filter Injection (5 minutes)

### 3.1 Check Filter Dropdown
1. [ ] Go to CRM Lead list
2. [ ] Click filter icon (funnel)
3. [ ] Click "Add Filter"
4. [ ] Look for "Order Source" in dropdown
5. [ ] "Order Source" should appear in list

**If not found:** 
- [ ] Refresh page
- [ ] Check browser console for errors
- [ ] Run: `window.debugCRMLeadColumns.checkOrderSourceField()`

### 3.2 Add Order Source Filter
1. [ ] Click "Add Filter"
2. [ ] Select "Order Source"
3. [ ] Select a source that has synced data
4. [ ] Click "Apply"

- [ ] Filter is applied
- [ ] Filter shows in filter bar
- [ ] No errors in console

---

## Phase 4: Test Column Filtering (10 minutes)

### 4.1 Verify Columns Show/Hide
1. [ ] With Order Source filter applied
2. [ ] Look at the list view columns
3. [ ] API columns from selected source should be visible
4. [ ] API columns from other sources should be hidden
5. [ ] Default columns (Name, Email, Status) should be visible

**If columns don't show/hide:**
- [ ] Run: `window.debugCRMLeadColumns.manuallyFilterColumns()`
- [ ] Check console output
- [ ] Continue to Phase 5

### 4.2 Test Filter Change
1. [ ] Change Order Source filter to different source
2. [ ] Columns should update instantly
3. [ ] No page reload should occur
4. [ ] New columns should be visible
5. [ ] Old columns should be hidden

- [ ] Filter change works
- [ ] Columns update instantly
- [ ] No errors in console

### 4.3 Test Filter Removal
1. [ ] Remove Order Source filter
2. [ ] All API columns should be hidden
3. [ ] Default columns should still be visible

- [ ] Filter removal works
- [ ] All API columns hidden
- [ ] Default columns visible

---

## Phase 5: Debug (if needed)

### 5.1 Check Current Filters
```javascript
window.debugCRMLeadColumns.getCurrentFilters()
```
- [ ] Command runs without errors
- [ ] Shows current filter state
- [ ] Order Source filter visible if applied
- [ ] Filter value matches selected source

### 5.2 Check List View Columns
```javascript
window.debugCRMLeadColumns.getListViewColumns()
```
- [ ] Command runs without errors
- [ ] Shows Fields array
- [ ] Shows DOM Column Headers count
- [ ] Shows list of columns with data-field attributes

### 5.3 Test CSS Application
```javascript
window.debugCRMLeadColumns.testCSSApplication()
```
- [ ] Command runs without errors
- [ ] Check if any columns turn red
- [ ] If columns turn red: CSS selectors work
- [ ] If no columns turn red: DOM structure issue

### 5.4 Manually Trigger Filtering
```javascript
window.debugCRMLeadColumns.manuallyFilterColumns()
```
- [ ] Command runs without errors
- [ ] Console shows "Selected Order Source"
- [ ] Console shows "Source Column Map"
- [ ] Console shows "Columns to show"
- [ ] Console shows "CSS applied"
- [ ] Columns update after command

### 5.5 Check All Custom Fields
```javascript
window.debugCRMLeadColumns.getAllCustomFields()
```
- [ ] Command runs without errors
- [ ] Shows all custom fields on CRM Lead
- [ ] API columns visible in list
- [ ] Order Source field visible in list

---

## Phase 6: Multi-Source Testing (10 minutes)

### 6.1 Sync Second API Source
1. [ ] Create/configure second Order Sync Source
2. [ ] Click "Sync Now"
3. [ ] Wait for completion
4. [ ] Check result shows "leads created"

### 6.2 Test Filtering with Multiple Sources
1. [ ] Go to CRM Lead list
2. [ ] Add Order Source filter
3. [ ] Select first source
4. [ ] Verify columns from first source visible
5. [ ] Change filter to second source
6. [ ] Verify columns from second source visible
7. [ ] Verify columns from first source hidden

- [ ] First source columns show correctly
- [ ] Second source columns show correctly
- [ ] Columns switch correctly when filter changes
- [ ] No errors in console

### 6.3 Test with No Filter
1. [ ] Remove Order Source filter
2. [ ] All API columns should be hidden
3. [ ] Default columns should be visible

- [ ] All API columns hidden
- [ ] Default columns visible

---

## Phase 7: Browser Compatibility (5 minutes)

### 7.1 Test on Chrome
- [ ] Open in Chrome
- [ ] Run through Phase 4 tests
- [ ] All tests pass

### 7.2 Test on Firefox
- [ ] Open in Firefox
- [ ] Run through Phase 4 tests
- [ ] All tests pass

### 7.3 Test on Safari (if available)
- [ ] Open in Safari
- [ ] Run through Phase 4 tests
- [ ] All tests pass

### 7.4 Test on Edge (if available)
- [ ] Open in Edge
- [ ] Run through Phase 4 tests
- [ ] All tests pass

---

## Phase 8: Error Handling (5 minutes)

### 8.1 Test with Invalid Filter
1. [ ] Add Order Source filter
2. [ ] Select a source with NO synced data
3. [ ] Columns should be hidden (no columns for that source)
4. [ ] No errors in console

### 8.2 Test with Deleted Source
1. [ ] Delete an Order Sync Source
2. [ ] Go to CRM Lead list
3. [ ] Try to filter by deleted source
4. [ ] System should handle gracefully
5. [ ] No errors in console

### 8.3 Test Page Refresh
1. [ ] Apply Order Source filter
2. [ ] Refresh page (F5)
3. [ ] Filter should persist
4. [ ] Columns should show/hide correctly
5. [ ] No errors in console

### 8.4 Test List Refresh
1. [ ] Apply Order Source filter
2. [ ] Click refresh button in list view
3. [ ] Columns should update correctly
4. [ ] No errors in console

---

## Phase 9: Performance Testing (5 minutes)

### 9.1 Test with Many Columns
1. [ ] Sync API with many columns (20+)
2. [ ] Add Order Source filter
3. [ ] Columns should show/hide quickly
4. [ ] No lag or delay
5. [ ] No errors in console

### 9.2 Test with Many Leads
1. [ ] Sync API with many leads (100+)
2. [ ] Go to CRM Lead list
3. [ ] Add Order Source filter
4. [ ] List should load quickly
5. [ ] Columns should show/hide quickly

### 9.3 Test Rapid Filter Changes
1. [ ] Apply Order Source filter
2. [ ] Quickly change filter multiple times
3. [ ] Columns should update correctly
4. [ ] No lag or errors
5. [ ] No console errors

---

## Phase 10: Final Verification (5 minutes)

### 10.1 Check Browser Console
- [ ] No red error messages
- [ ] No warnings about missing elements
- [ ] No warnings about failed API calls

### 10.2 Check Server Logs
```bash
bench --site <your-site> tail -f
```
- [ ] No errors related to Order Integration
- [ ] No errors related to API Schema Storage
- [ ] No errors related to Custom Fields

### 10.3 Check Database
```sql
SELECT COUNT(*) FROM `tabCustom Field` WHERE fieldname LIKE 'api_col_%';
```
- [ ] Count matches number of API columns created
- [ ] All fields have correct description

### 10.4 Final Checklist
- [ ] Order Source field exists
- [ ] API columns created
- [ ] Leads have data
- [ ] Filter appears in dropdown
- [ ] Columns show/hide correctly
- [ ] Filter changes work
- [ ] Multiple sources work
- [ ] No errors in console
- [ ] No errors in logs
- [ ] Performance is good

---

## Test Results Summary

### Overall Status
- [ ] All tests passed
- [ ] System is ready for production

### Issues Found
- [ ] Issue 1: _______________
- [ ] Issue 2: _______________
- [ ] Issue 3: _______________

### Notes
```
[Add any notes or observations here]
```

---

## Sign-Off

- **Tested By:** _______________
- **Date:** _______________
- **Status:** ✅ Ready / ❌ Not Ready
- **Comments:** _______________

---

## If Tests Failed

1. [ ] Document the issue
2. [ ] Run debug commands
3. [ ] Check browser console
4. [ ] Check server logs
5. [ ] Follow troubleshooting guide in COLUMN_FILTERING_GUIDE.md
6. [ ] Provide debug output if needed

---

## Next Steps

If all tests pass:
- [ ] System is ready for production
- [ ] Users can start syncing APIs
- [ ] Columns will auto-filter based on Order Source

If tests failed:
- [ ] Follow troubleshooting guide
- [ ] Fix identified issues
- [ ] Re-run tests
- [ ] Repeat until all tests pass

