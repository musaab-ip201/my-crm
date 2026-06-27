# Quick Start - Column Filtering

## 30-Second Setup

1. **Sync an API source:**
   - Go to Order Sync Sources
   - Select a source
   - Click "Sync Now"
   - Wait for completion

2. **Go to CRM Lead list:**
   - URL: `/app/crm-lead`

3. **Add Order Source filter:**
   - Click filter icon (funnel)
   - Click "Add Filter"
   - Select "Order Source"
   - Select the source you just synced
   - Click "Apply"

4. **Done!**
   - API columns from that source should now be visible
   - Columns from other sources are hidden
   - Default columns (Name, Email, Status) are always visible

---

## Debug Commands (Copy & Paste)

Open browser console (F12) and paste these:

### Check if everything is set up:
```javascript
window.debugCRMLeadColumns.help()
```

### Check Order Source field:
```javascript
window.debugCRMLeadColumns.checkOrderSourceField()
```

### Check API columns:
```javascript
window.debugCRMLeadColumns.getAllApiColumns()
```

### Check current filters:
```javascript
window.debugCRMLeadColumns.getCurrentFilters()
```

### Manually trigger filtering:
```javascript
window.debugCRMLeadColumns.manuallyFilterColumns()
```

### Test CSS application:
```javascript
window.debugCRMLeadColumns.testCSSApplication()
```

---

## Common Issues

### "I don't see the Order Source filter"
- Make sure you've synced at least one API source first
- Refresh the page
- Check browser console for errors

### "I added the filter but columns don't show/hide"
- Run: `window.debugCRMLeadColumns.manuallyFilterColumns()`
- Check console output for errors
- Make sure you synced data from that source

### "I don't see API columns in 'Add Column' dropdown"
- Sync an API source first
- Go to Order Sync Sources → Select source → Click "Sync Now"
- Refresh the page
- Try "Add Column" again

### "Columns show but with wrong data"
- Make sure the Order Source filter is set correctly
- Check if the lead has data in that column
- Manually add the column to verify data

---

## How It Works

1. **When you sync an API:**
   - Columns are automatically detected from API response
   - Custom fields are created on CRM Lead
   - Leads are created with data in those fields

2. **When you select Order Source filter:**
   - Script detects the filter value
   - Script hides all API columns
   - Script shows only columns from selected source
   - No page reload needed

3. **When you change the filter:**
   - Script detects the change
   - Columns are instantly updated
   - No page reload needed

---

## What You'll See

### Before selecting filter:
- Default columns: Name, Email, Status, Assigned To, Modified
- API columns: Hidden

### After selecting filter:
- Default columns: Still visible
- API columns from selected source: Visible
- API columns from other sources: Hidden

### When you change filter:
- Columns update instantly
- No page reload
- Smooth transition

---

## Need Help?

1. **Check the full guide:**
   - Read: `COLUMN_FILTERING_GUIDE.md`

2. **Check the technical summary:**
   - Read: `FILTERING_FIX_SUMMARY.md`

3. **Run debug commands:**
   - Open browser console (F12)
   - Run: `window.debugCRMLeadColumns.help()`
   - Follow the output

4. **Check server logs:**
   ```bash
   bench --site <your-site> tail -f
   ```

---

## Files to Know About

- `public/js/crm_lead_column_manager.js` - Main filtering logic
- `public/js/crm_lead_list_debug.js` - Debug functions
- `public/js/lead_source_filter.js` - Filter injection
- `boot.py` - Script loading configuration
- `COLUMN_FILTERING_GUIDE.md` - Full testing guide
- `FILTERING_FIX_SUMMARY.md` - Technical details

