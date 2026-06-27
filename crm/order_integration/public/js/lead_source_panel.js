/**
 * lead_source_panel.js
 *
 * Injects a "Source Data" panel into the CRM Lead detail page right sidebar.
 * When a lead has an order_source linked, the panel shows:
 *   - A dropdown to select data type (Cart Data, Ticket Data, …)
 *   - A dynamic table with columns specific to the chosen data type
 *
 * Injected via boot.py after_request hook — no CRM source files modified.
 */
;(function () {
  'use strict'

  var PANEL_ID = 'oi-lead-source-panel'
  var STYLE_ID = 'oi-lead-source-panel-styles'

  // ── Styles ─────────────────────────────────────────────────────────────────
  function injectStyles() {
    if (document.getElementById(STYLE_ID)) return
    var s = document.createElement('style')
    s.id = STYLE_ID
    s.textContent = [
      '#' + PANEL_ID + ' { border-top: 1px solid var(--outline-gray-modals, #e5e7eb); padding: 12px 16px; font-size: 13px; }',
      '#' + PANEL_ID + ' .oi-panel-title { font-weight: 600; color: var(--ink-gray-7, #374151); margin-bottom: 10px; display: flex; align-items: center; gap: 6px; }',
      '#' + PANEL_ID + ' .oi-select { width: 100%; padding: 6px 8px; border: 1px solid var(--outline-gray-2, #d1d5db); border-radius: 6px; font-size: 12px; background: var(--surface-white, #fff); color: var(--ink-gray-8, #1f2937); cursor: pointer; outline: none; margin-bottom: 10px; }',
      '#' + PANEL_ID + ' .oi-select:focus { border-color: var(--outline-blue-3, #3b82f6); box-shadow: 0 0 0 2px var(--surface-blue-1, #eff6ff); }',
      '#' + PANEL_ID + ' .oi-load-btn { display: inline-flex; align-items: center; gap: 4px; padding: 5px 12px; background: var(--ink-gray-8, #1f2937); color: #fff; border: none; border-radius: 6px; font-size: 12px; cursor: pointer; margin-bottom: 10px; }',
      '#' + PANEL_ID + ' .oi-load-btn:hover { opacity: 0.85; }',
      '#' + PANEL_ID + ' .oi-load-btn:disabled { opacity: 0.5; cursor: not-allowed; }',
      '#' + PANEL_ID + ' .oi-table-wrap { overflow-x: auto; border: 1px solid var(--outline-gray-2, #e5e7eb); border-radius: 6px; max-height: 320px; overflow-y: auto; }',
      '#' + PANEL_ID + ' table { width: 100%; border-collapse: collapse; font-size: 11px; }',
      '#' + PANEL_ID + ' thead { background: var(--surface-gray-2, #f3f4f6); position: sticky; top: 0; z-index: 1; }',
      '#' + PANEL_ID + ' th { padding: 6px 8px; text-align: left; font-weight: 600; color: var(--ink-gray-6, #4b5563); white-space: nowrap; border-bottom: 1px solid var(--outline-gray-2, #e5e7eb); }',
      '#' + PANEL_ID + ' td { padding: 5px 8px; color: var(--ink-gray-8, #1f2937); border-bottom: 1px solid var(--outline-gray-1, #f3f4f6); max-width: 160px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }',
      '#' + PANEL_ID + ' tr:last-child td { border-bottom: none; }',
      '#' + PANEL_ID + ' tr:hover td { background: var(--surface-gray-1, #f9fafb); }',
      '#' + PANEL_ID + ' .oi-empty { color: var(--ink-gray-4, #9ca3af); font-size: 12px; padding: 12px 0; text-align: center; }',
      '#' + PANEL_ID + ' .oi-error { color: #dc2626; font-size: 12px; padding: 8px; background: #fef2f2; border-radius: 4px; margin-bottom: 8px; }',
      '#' + PANEL_ID + ' .oi-spinner { display: inline-block; width: 14px; height: 14px; border: 2px solid #e5e7eb; border-top-color: #3b82f6; border-radius: 50%; animation: oi-spin 0.7s linear infinite; vertical-align: middle; }',
      '@keyframes oi-spin { to { transform: rotate(360deg); } }',
      '#' + PANEL_ID + ' .oi-badge { display: inline-block; padding: 1px 6px; border-radius: 9999px; font-size: 10px; font-weight: 600; background: var(--surface-blue-1, #eff6ff); color: var(--ink-blue-4, #2563eb); margin-left: 4px; }',
      '#' + PANEL_ID + ' .oi-pagination { display: flex; align-items: center; justify-content: space-between; margin-top: 8px; font-size: 11px; color: var(--ink-gray-5, #6b7280); }',
      '#' + PANEL_ID + ' .oi-pg-btn { padding: 3px 8px; border: 1px solid var(--outline-gray-2, #d1d5db); border-radius: 4px; background: var(--surface-white, #fff); cursor: pointer; font-size: 11px; }',
      '#' + PANEL_ID + ' .oi-pg-btn:disabled { opacity: 0.4; cursor: not-allowed; }',
      '#' + PANEL_ID + ' .oi-no-source { color: var(--ink-gray-4, #9ca3af); font-size: 12px; font-style: italic; }',
    ].join('\n')
    document.head.appendChild(s)
  }

  // ── CSRF token helper ───────────────────────────────────────────────────────
  function getCsrf() {
    try {
      if (typeof frappe !== 'undefined' && frappe.get_cookie) {
        var token = frappe.get_cookie('csrf_token')
        if (token) return token
      }

      var cookies = document.cookie.split(';')
      for (var i = 0; i < cookies.length; i++) {
        var c = cookies[i].trim()
        if (c.startsWith('csrf_token=')) return c.slice('csrf_token='.length)
      }
    } catch (e) {}
    return ''
  }

  function serializeArgs(args) {
    var parts = []
    if (!args) return ''
    Object.keys(args).forEach(function (key) {
      var value = args[key]
      if (value === undefined || value === null) return
      if (typeof value === 'object') {
        value = JSON.stringify(value)
      }
      parts.push(encodeURIComponent(key) + '=' + encodeURIComponent(value))
    })
    return parts.join('&')
  }

  // ── Frappe API call ─────────────────────────────────────────────────────────
  function apiCall(method, args) {
    if (typeof frappe !== 'undefined' && frappe.call) {
      return new Promise(function (resolve, reject) {
        frappe.call({
          method: method,
          args: args || {},
          freeze: false,
          callback: function (r) {
            if (r.exc) {
              return reject(new Error(r.exc))
            }
            resolve(r.message)
          },
          error: function (xhr) {
            var msg = 'API request failed'
            try {
              var data = JSON.parse(xhr.responseText)
              if (data.exc) msg = data.exc
              else if (data.message) msg = data.message
            } catch (e) {}
            reject(new Error(msg))
          }
        })
      })
    }

    var token = getCsrf()
    var url = '/api/method/' + encodeURIComponent(method)
    if (!token) {
      var query = serializeArgs(args || {})
      if (query) {
        url += '?' + query
      }
      return fetch(url, {
        method: 'GET',
        credentials: 'same-origin',
      })
        .then(function (r) { return r.json() })
        .then(function (d) {
          if (d.exc) throw new Error(d.exc)
          return d.message
        })
    }

    return fetch(url, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': token,
      },
      body: JSON.stringify(args || {}),
    })
      .then(function (r) { return r.json() })
      .then(function (d) {
        if (d.exc) throw new Error(d.exc)
        return d.message
      })
  }

  // ── Get current lead ID from URL ────────────────────────────────────────────
  function getLeadIdFromUrl() {
    // URL pattern: /crm/leads/<leadId>
    var m = window.location.pathname.match(/\/crm\/leads\/([^/?#]+)/)
    return m ? decodeURIComponent(m[1]) : null
  }

  // ── Panel state ─────────────────────────────────────────────────────────────
  var state = {
    leadId: null,
    dataTypes: [],       // [{value, label}]
    selectedType: '',
    records: [],
    columns: [],
    loading: false,
    error: '',
    page: 1,
    pageSize: 20,
    totalRecords: 0,
  }

  // ── Render helpers ──────────────────────────────────────────────────────────
  function formatCell(val) {
    if (val === null || val === undefined) return '—'
    var s = String(val)
    if (s.length > 60) return s.substring(0, 57) + '…'
    return s
  }

  function renderPanel(panel) {
    panel.innerHTML = ''

    // Title
    var title = document.createElement('div')
    title.className = 'oi-panel-title'
    title.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg> Source Data'
    panel.appendChild(title)

    // No source linked
    if (!state.leadId) {
      var ns = document.createElement('div')
      ns.className = 'oi-no-source'
      ns.textContent = 'No lead loaded.'
      panel.appendChild(ns)
      return
    }

    // Error
    if (state.error) {
      var err = document.createElement('div')
      err.className = 'oi-error'
      err.textContent = state.error
      panel.appendChild(err)
    }

    // Data type selector
    var sel = document.createElement('select')
    sel.className = 'oi-select'

    var placeholder = document.createElement('option')
    placeholder.value = ''
    placeholder.textContent = '— Select data type —'
    sel.appendChild(placeholder)

    state.dataTypes.forEach(function (dt) {
      var opt = document.createElement('option')
      opt.value = dt.value
      opt.textContent = dt.label
      if (dt.value === state.selectedType) opt.selected = true
      sel.appendChild(opt)
    })

    sel.addEventListener('change', function () {
      state.selectedType = sel.value
      state.records = []
      state.columns = []
      state.error = ''
      state.page = 1
      renderPanel(panel)
    })
    panel.appendChild(sel)

    // Load button
    if (state.selectedType) {
      var loadBtn = document.createElement('button')
      loadBtn.className = 'oi-load-btn'
      loadBtn.disabled = state.loading
      loadBtn.innerHTML = state.loading
        ? '<span class="oi-spinner"></span> Loading…'
        : '↓ Load Data'
      loadBtn.addEventListener('click', function () {
        state.page = 1
        loadData(panel)
      })
      panel.appendChild(loadBtn)
    }

    // Table
    if (state.records.length > 0) {
      var wrap = document.createElement('div')
      wrap.className = 'oi-table-wrap'

      var table = document.createElement('table')

      // thead
      var thead = document.createElement('thead')
      var headerRow = document.createElement('tr')
      state.columns.forEach(function (col) {
        var th = document.createElement('th')
        th.textContent = col.replace(/_/g, ' ').replace(/\./g, ' › ')
        headerRow.appendChild(th)
      })
      thead.appendChild(headerRow)
      table.appendChild(thead)

      // tbody
      var tbody = document.createElement('tbody')
      state.records.forEach(function (rec) {
        var tr = document.createElement('tr')
        state.columns.forEach(function (col) {
          var td = document.createElement('td')
          td.title = String(rec[col] !== undefined && rec[col] !== null ? rec[col] : '')
          td.textContent = formatCell(rec[col])
          tr.appendChild(td)
        })
        tbody.appendChild(tr)
      })
      table.appendChild(tbody)
      wrap.appendChild(table)
      panel.appendChild(wrap)

      // Pagination
      var pg = document.createElement('div')
      pg.className = 'oi-pagination'

      var info = document.createElement('span')
      info.textContent = 'Page ' + state.page + ' · ' + state.records.length + ' records'
      pg.appendChild(info)

      var pgBtns = document.createElement('div')
      pgBtns.style.display = 'flex'
      pgBtns.style.gap = '4px'

      var prevBtn = document.createElement('button')
      prevBtn.className = 'oi-pg-btn'
      prevBtn.textContent = '‹ Prev'
      prevBtn.disabled = state.page <= 1
      prevBtn.addEventListener('click', function () {
        if (state.page > 1) { state.page--; loadData(panel) }
      })
      pgBtns.appendChild(prevBtn)

      var nextBtn = document.createElement('button')
      nextBtn.className = 'oi-pg-btn'
      nextBtn.textContent = 'Next ›'
      nextBtn.disabled = state.records.length < state.pageSize
      nextBtn.addEventListener('click', function () {
        state.page++; loadData(panel)
      })
      pgBtns.appendChild(nextBtn)

      pg.appendChild(pgBtns)
      panel.appendChild(pg)

    } else if (!state.loading && state.selectedType && !state.error) {
      var empty = document.createElement('div')
      empty.className = 'oi-empty'
      empty.textContent = 'No records found for this customer.'
      panel.appendChild(empty)
    }
  }

  // ── Load data from API ──────────────────────────────────────────────────────
  function loadData(panel) {
    if (!state.selectedType || !state.leadId) return
    state.loading = true
    state.error = ''
    renderPanel(panel)

    apiCall(
      'order_integration.order_integration.api.lead_source_data_api.get_lead_source_data',
      {
        lead_name: state.leadId,
        data_type: state.selectedType,
        page: state.page,
        page_size: state.pageSize,
      }
    )
      .then(function (result) {
        state.loading = false
        if (result && result.status === 'success') {
          state.records = result.records || []
          state.columns = result.columns || []
          state.totalRecords = result.total_records || 0
          state.error = ''
        } else {
          state.error = (result && result.message) || 'Failed to load data'
          state.records = []
          state.columns = []
        }
        renderPanel(panel)
      })
      .catch(function (e) {
        state.loading = false
        state.error = e.message || 'An error occurred'
        state.records = []
        state.columns = []
        renderPanel(panel)
      })
  }

  // ── Load data types from API ────────────────────────────────────────────────
  function detectBestDataType(panel, index) {
    if (!state.dataTypes || index >= state.dataTypes.length) {
      renderPanel(panel)
      return
    }

    var type = state.dataTypes[index]
    state.selectedType = type.value
    apiCall('order_integration.order_integration.api.lead_source_data_api.get_lead_source_data', {
      lead_name: state.leadId,
      data_type: state.selectedType,
      page: state.page,
      page_size: state.pageSize,
    })
      .then(function (result) {
        if (result && result.status === 'success' && result.records && result.records.length > 0) {
          state.records = result.records || []
          state.columns = result.columns || []
          state.totalRecords = result.total_records || 0
          state.error = ''
          renderPanel(panel)
          return
        }

        state.records = []
        state.columns = []
        state.totalRecords = 0
        state.error = ''

        detectBestDataType(panel, index + 1)
      })
      .catch(function () {
        state.records = []
        state.columns = []
        state.totalRecords = 0
        state.error = ''
        detectBestDataType(panel, index + 1)
      })
  }

  function loadDataTypes(panel) {
    apiCall('order_integration.order_integration.api.lead_source_data_api.get_data_types', {
      lead_name: state.leadId,
    })
      .then(function (types) {
        state.dataTypes = types || []

        // Auto-select and auto-load when only one type available
        if (state.dataTypes.length === 1) {
          state.selectedType = state.dataTypes[0].value
          renderPanel(panel)
          loadData(panel)
          return
        }

        // Multiple types — auto-detect which one has data for this lead
        if (state.dataTypes.length > 1) {
          renderPanel(panel)
          detectBestDataType(panel, 0)
          return
        }

        renderPanel(panel)
      })
      .catch(function () {
        state.dataTypes = [
          { value: 'cart_data', label: 'Cart Data' },
          { value: 'ticket_data', label: 'Ticket Data' },
        ]
        renderPanel(panel)
      })
  }

  // ── Find the right sidebar in the Lead page ─────────────────────────────────
  function findLeadSidebar() {
    // Try multiple selectors in order of specificity
    var selectors = [
      '[class*="border-l"]',
      '[class*="sidebar"]',
      '[class*="right-panel"]',
      '[class*="details-panel"]',
    ]

    for (var s = 0; s < selectors.length; s++) {
      var candidates = document.querySelectorAll(selectors[s])
      for (var i = 0; i < candidates.length; i++) {
        var el = candidates[i]
        // Must look like the lead sidebar — has avatar, copy-able ID, or activity section
        if (
          el.querySelector('.size-12') ||
          el.querySelector('[class*="cursor-copy"]') ||
          el.querySelector('[class*="avatar"]') ||
          el.querySelector('[class*="activity"]')
        ) {
          return el
        }
      }
    }

    // Last resort: any scrollable right-side panel
    var all = document.querySelectorAll('[class*="overflow-y-auto"]')
    for (var i = 0; i < all.length; i++) {
      var rect = all[i].getBoundingClientRect()
      // Must be on the right half of the screen and reasonably tall
      if (rect.left > window.innerWidth * 0.5 && rect.height > 200) {
        return all[i]
      }
    }

    return null
  }

  // ── Inject panel into sidebar ───────────────────────────────────────────────
  function injectPanel() {
    var leadId = getLeadIdFromUrl()
    if (!leadId) return false

    var sidebar = findLeadSidebar()
    if (!sidebar) return false

    // Remove stale panel
    var old = document.getElementById(PANEL_ID)
    if (old) {
      // If same lead, don't re-inject
      if (state.leadId === leadId) return true
      old.remove()
    }

    // Reset state for new lead
    state.leadId = leadId
    state.selectedType = ''
    state.records = []
    state.columns = []
    state.error = ''
    state.page = 1
    state.dataTypes = []

    var panel = document.createElement('div')
    panel.id = PANEL_ID

    // Append at the bottom of the sidebar
    sidebar.appendChild(panel)

    // Initial render (empty)
    renderPanel(panel)

    // Load data types
    loadDataTypes(panel)

    return true
  }

  // ── Watch for URL changes (SPA navigation) ──────────────────────────────────
  function watchNavigation() {
    var lastPath = window.location.pathname

    // Poll for URL changes
    setInterval(function () {
      var currentPath = window.location.pathname
      if (currentPath !== lastPath) {
        lastPath = currentPath
        // Small delay to let Vue render the new page
        setTimeout(function () {
          if (currentPath.match(/\/crm\/leads\/[^/?#]+/)) {
            injectPanel()
          } else {
            // Remove panel if navigated away from lead page
            var old = document.getElementById(PANEL_ID)
            if (old) old.remove()
            state.leadId = null
          }
        }, 800)
      }
    }, 300)
  }

  // ── MutationObserver for DOM readiness ──────────────────────────────────────
  function startObserver() {
    var injected = false
    var timer = null

    var observer = new MutationObserver(function () {
      if (!window.location.pathname.match(/\/crm\/leads\/[^/?#]+/)) return
      clearTimeout(timer)
      timer = setTimeout(function () {
        if (!document.getElementById(PANEL_ID)) {
          injected = injectPanel()
        }
      }, 600)
    })

    observer.observe(document.body, { childList: true, subtree: true })
  }

  // ── Bootstrap ───────────────────────────────────────────────────────────────
  function init() {
    injectStyles()
    startObserver()
    watchNavigation()

    // Try immediate injection if already on a lead page
    if (window.location.pathname.match(/\/crm\/leads\/[^/?#]+/)) {
      setTimeout(injectPanel, 1800)
    }
  }

  function waitForReady() {
    if (typeof frappe !== 'undefined' && frappe.boot) {
      init()
      return
    }
    var n = 0
    var t = setInterval(function () {
      if (typeof frappe !== 'undefined' && frappe.boot) {
        clearInterval(t)
        init()
      } else if (++n > 80) {
        clearInterval(t)
        init()
      }
    }, 200)
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', waitForReady)
  } else {
    waitForReady()
  }
})()
