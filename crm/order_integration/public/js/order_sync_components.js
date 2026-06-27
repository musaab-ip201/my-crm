window.toast = {
  show: (msg, type = 'info') => {
    const colors = {
      success: '#22c55e',
      error: '#ef4444',
      warning: '#f59e0b',
      info: '#3b82f6'
    }

    const el = document.createElement('div')
    el.innerText = msg

    el.style.position = 'fixed'
    el.style.top = '20px'
    el.style.right = '20px'
    el.style.background = colors[type] || colors.info
    el.style.color = '#fff'
    el.style.padding = '10px 14px'
    el.style.borderRadius = '6px'
    el.style.zIndex = '99999'
    el.style.boxShadow = '0 4px 10px rgba(0,0,0,0.1)'
    el.style.fontSize = '14px'

    document.body.appendChild(el)

    setTimeout(() => {
      el.style.opacity = '0'
      el.style.transition = 'opacity 0.3s'
    }, 2500)

    setTimeout(() => {
      el.remove()
    }, 3000)
  },

  success: (msg) => toast.show(msg, 'success'),
  error: (msg) => toast.show(msg, 'error'),
  warning: (msg) => toast.show(msg, 'warning'),
  info: (msg) => toast.show(msg, 'info'),
}

/**
 * order_sync_components.js
 *
 * Order Syncing UI — uses the CRM's Vue app context to access frappe-ui's call function.
 */
;(function () {
  'use strict'

  // ── Get the call function from the CRM's Vue app ────────────────────────
  function getCallFunction() {
    try {
      // Try to get from the Vue app instance
      var appEl = document.getElementById('app')
      if (appEl && appEl.__vue_app__) {
        var app = appEl.__vue_app__
        // frappe-ui's call is injected as a global property
        if (app.config && app.config.globalProperties && app.config.globalProperties.$call) {
          return app.config.globalProperties.$call
        }
      }
    } catch (e) {
      console.log('[OrderSync] Could not get call from Vue app:', e)
    }

    // Fallback: return null and we'll use fetch
    return null
  }

  // ── API call wrapper ───────────────────────────────────────────────────────
  function apiCall(method, args) {
    return new Promise(function (resolve, reject) {
      var callFn = getCallFunction()

      if (callFn && typeof callFn === 'function') {
        try {
          var promise = callFn(method, args || {})

          if (promise && typeof promise.then === 'function') {
            promise
              .then(function (result) {
                resolve(result)
              })
              .catch(function (error) {
                reject(error)
              })
          } else {
            resolve(promise)
          }
        } catch (e) {
          reject(e)
        }
        return
      }

      // Fallback: use fetch API directly
      var url = '/api/method/' + method
      var csrfToken = ''

      // Try to get CSRF token
      try {
        var cookies = document.cookie.split(';')
        for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim()
          if (cookie.startsWith('csrf_token=')) {
            csrfToken = cookie.substring('csrf_token='.length)
            break
          }
        }
      } catch (e) {}

      var options = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(args || {})
      }

      if (csrfToken) {
        options.headers['X-Frappe-CSRF-Token'] = csrfToken
      }

      fetch(url, options)
        .then(function (response) {
          if (!response.ok) {
            throw new Error('HTTP ' + response.status)
          }
          return response.json()
        })
        .then(function (data) {
          if (data.exc) {
            throw new Error(data.exc)
          }
          resolve(data.message)
        })
        .catch(function (error) {
          reject(error)
        })
    })
  }

function showAlert(msg, type = 'info') {
  if (window.toast) {
    if (type === 'success') {
      toast.success(msg)
    } else if (type === 'error') {
      toast.error(msg)
    } else if (type === 'warning') {
      toast.warning(msg)
    } else {
      toast.info(msg)
    }
    return
  }

  // fallback (only if toast somehow not loaded)
  console.warn('Toast not available, fallback alert:', msg)
  alert(msg)
}
  // ── CSS ────────────────────────────────────────────────────────────────────
  function injectStyles() {
    if (document.getElementById('order-sync-styles')) return
    var style = document.createElement('style')
    style.id = 'order-sync-styles'
    style.textContent = [
      '.os-page { display:flex; flex-direction:column; height:100%; padding:24px; gap:24px; font-family:inherit; color:var(--ink-gray-8); }',
      '.os-header { display:flex; justify-content:space-between; align-items:flex-start; }',
      '.os-title { font-size:1.25rem; font-weight:600; display:flex; align-items:center; gap:8px; }',
      '.os-badge { background:var(--surface-amber-1); color:var(--ink-amber-5); font-size:0.7rem; font-weight:600; padding:2px 8px; border-radius:9999px; border:1px solid var(--outline-amber-2); }',
      '.os-subtitle { font-size:0.875rem; color:var(--ink-gray-6); margin-top:4px; }',
      '.os-btn { display:inline-flex; align-items:center; gap:6px; padding:6px 14px; border-radius:6px; font-size:0.875rem; font-weight:500; cursor:pointer; border:none; transition:opacity .15s; }',
      '.os-btn:hover { opacity:0.85; }',
      '.os-btn-solid { background:var(--ink-gray-8); color:var(--surface-white); }',
      '.os-btn-outline { background:var(--surface-white); color:var(--ink-gray-8); border:1px solid var(--outline-gray-2); }',
      '.os-btn-ghost { background:transparent; color:var(--ink-gray-7); }',
      '.os-btn-ghost:hover { background:var(--surface-gray-1); }',
      '.os-btn-back { background:transparent; border:none; font-size:1.1rem; font-weight:600; color:var(--ink-gray-8); cursor:pointer; display:flex; align-items:center; gap:4px; padding:4px 0; }',
      '.os-btn-back:hover { opacity:0.7; }',
      '.os-empty { border:2px dashed var(--outline-gray-2); border-radius:8px; display:flex; align-items:center; justify-content:center; min-height:200px; color:var(--ink-gray-4); font-size:0.9rem; margin:0 8px; }',
      '.os-table-header { display:flex; padding:8px 16px; font-size:0.8rem; color:var(--ink-gray-4); }',
      '.os-divider { height:1px; background:var(--outline-gray-modals); margin:0 16px; }',
      '.os-row { display:flex; align-items:center; padding:12px; cursor:pointer; border-radius:6px; transition:background .1s; }',
      '.os-row:hover { background:var(--surface-menu-bar); }',
      '.os-col-6 { width:60%; padding-right:16px; overflow:hidden; }',
      '.os-col-2 { width:20%; padding-right:16px; overflow:hidden; }',
      '.os-col-2-end { width:20%; display:flex; align-items:center; justify-content:space-between; }',
      '.os-text-main { font-size:0.875rem; font-weight:500; color:var(--ink-gray-7); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }',
      '.os-text-sub { font-size:0.8rem; color:var(--ink-gray-4); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }',
      '.os-form { display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:24px; padding:0 8px; }',
      '.os-form-full { grid-column:1/-1; }',
      '.os-field { display:flex; flex-direction:column; gap:4px; }',
      '.os-label { font-size:0.8rem; font-weight:500; color:var(--ink-gray-6); }',
      '.os-input { padding:7px 10px; border:1px solid var(--outline-gray-2); border-radius:6px; font-size:0.875rem; outline:none; width:100%; box-sizing:border-box; background:var(--surface-white); color:var(--ink-gray-8); }',
      '.os-input::placeholder { color:var(--ink-gray-4); }',
      '.os-input:focus { border-color:var(--outline-blue-3); box-shadow:0 0 0 2px var(--surface-blue-1); }',
      '.os-select { padding:7px 10px; border:1px solid var(--outline-gray-2); border-radius:6px; font-size:0.875rem; outline:none; width:100%; box-sizing:border-box; background:var(--surface-white); color:var(--ink-gray-8); cursor:pointer; }',
      '.os-actions { display:flex; gap:8px; }',
      '.os-menu { position:relative; display:inline-block; }',
      '.os-menu-btn { background:transparent; border:none; cursor:pointer; padding:4px 6px; border-radius:4px; color:var(--ink-gray-5); font-size:1.1rem; line-height:1; }',
      '.os-menu-btn:hover { background:var(--surface-gray-1); }',
     '.os-menu-dropdown {position: absolute !important; right: 0 !important;left: auto !important;top: calc(100% + 4px) !important;transform: none !important;background: var(--surface-menu-bar, var(--surface-white));border: 1px solid var(--border-color, #e5e7eb);border-radius: 8px;box-shadow: 0 4px 16px rgba(0,0,0,.12);min-width: 160px;z-index: 99999;padding: 4px;color: var(--text-color, inherit);}',
     '.os-menu-item {display: flex;align-items: center;gap: 8px;padding: 8px 12px; font-size: 0.875rem;cursor: pointer;border-radius: 6px;color: var(--ink-gray-7);}',
      '.os-menu-item:hover { background:var(--surface-gray-1); }',
      '.os-menu-item.danger { color:var(--ink-red-4); }',
      '.os-menu-item.danger:hover { background:var(--surface-red-1); }',
      '.os-spinner { display:inline-block; width:20px; height:20px; border:2px solid var(--outline-gray-2); border-top-color:var(--outline-blue-3); border-radius:50%; animation:os-spin .7s linear infinite; }',
      '@keyframes os-spin { to { transform:rotate(360deg); } }',
      '.os-loading { display:flex; justify-content:center; align-items:center; padding:60px; }',
      '.os-test-btn { width:100%; justify-content:center; }',
    ].join('\n')
    document.head.appendChild(style)
  }

  // ── DOM helpers ────────────────────────────────────────────────────────────
  function el(tag, attrs, children) {
    var node = document.createElement(tag)
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === 'class') node.className = attrs[k]
        else if (k === 'style') node.style.cssText = attrs[k]
        else if (k.startsWith('on')) node.addEventListener(k.slice(2).toLowerCase(), attrs[k])
        else if (k === 'type' && tag === 'input') node.type = attrs[k]
        else if (k === 'placeholder') node.placeholder = attrs[k]
        else if (k === 'value') node.value = attrs[k]
        else if (k === 'disabled') { if (attrs[k]) node.disabled = true }
        else node.setAttribute(k, attrs[k])
      })
    }
    if (children) {
      if (typeof children === 'string') node.textContent = children
      else if (Array.isArray(children)) children.forEach(function (c) { if (c) node.appendChild(c) })
      else node.appendChild(children)
    }
    return node
  }

  function btn(label, cls, onClick, icon) {
    var b = el('button', { class: 'os-btn ' + cls, onClick: onClick })
    if (icon) b.innerHTML = icon + ' '
    b.appendChild(document.createTextNode(label))
    return b
  }

  function spinner() {
    return el('div', { class: 'os-loading' }, el('div', { class: 'os-spinner' }))
  }

  function formatDate(dt) {
    if (!dt) return 'Never'
    return new Date(dt).toLocaleDateString()
  }

  // ── Sources List view ──────────────────────────────────────────────────────
  function renderSourcesList(container, onNew, onEdit) {
    container.innerHTML = ''
    container.appendChild(spinner())

    apiCall(
      'order_integration.order_integration.doctype.order_sync_source.order_sync_source.get_order_sources'
    ).then(function (sources) {
      sources = sources || []
      container.innerHTML = ''

      var page = el('div', { class: 'os-page' })

      // Header
      var header = el('div', { class: 'os-header' })
      var left = el('div', {})
      var titleRow = el('div', { class: 'os-title' })
      titleRow.appendChild(document.createTextNode('Order sources'))
      titleRow.appendChild(el('span', { class: 'os-badge' }, 'Beta'))
      left.appendChild(titleRow)
      left.appendChild(el('p', { class: 'os-subtitle' }, 'Manage sources for automatic order syncing to your CRM'))
      header.appendChild(left)

      var actions = el('div', { class: 'os-actions' })
      var syncAllBtn = btn('Sync All', 'os-btn-outline', function () {
        syncAllBtn.disabled = true
        syncAllBtn.textContent = 'Syncing...'
        apiCall(
          'order_integration.order_integration.doctype.order_sync_source.order_sync_source.trigger_sync_all'
        ).then(function (result) {
          syncAllBtn.disabled = false
          syncAllBtn.textContent = 'Sync All'
          if (result && result.status === 'success') {
            toast.success(result.message || 'All sources synced')
          } else if (result && result.status === 'error') {
            toast.error('Sync failed: ' + (result.message || 'Unknown error'))
          } else {
            toast.success('Sync completed')
          }
        }).catch(function (err) {
          toast.error('Sync failed: ' + (err && err.message ? err.message : String(err)))
          syncAllBtn.disabled = false
          syncAllBtn.textContent = 'Sync All'
        })
      }, '↻')
      actions.appendChild(syncAllBtn)
      actions.appendChild(btn('+ New', 'os-btn-solid', onNew))
      header.appendChild(actions)
      page.appendChild(header)

      if (!sources.length) {
        page.appendChild(el('div', { class: 'os-empty' }, 'No order sources found. Click New to add one.'))
      } else {
        // Table header
        var th = el('div', { class: 'os-table-header' })
        th.innerHTML = '<div style="width:60%">Name</div><div style="width:20%">API Key</div><div style="width:20%">Last Synced</div>'
        page.appendChild(th)
        page.appendChild(el('div', { class: 'os-divider' }))

        var list = el('ul', { style: 'list-style:none;margin:0;padding:8px;' })
        sources.forEach(function (source, i) {
          var row = el('li', { class: 'os-row', onClick: function () { onEdit(source) } })

          var nameCol = el('div', { class: 'os-col-6' })
          nameCol.appendChild(el('div', { class: 'os-text-main' }, source.source_name || source.name))
          row.appendChild(nameCol)

          var apiKeyCol = el('div', { class: 'os-col-2' })
          apiKeyCol.appendChild(el('div', { class: 'os-text-sub' }, source.api_key || ''))
          row.appendChild(apiKeyCol)

          var lastCol = el('div', { class: 'os-col-2-end' })
          lastCol.appendChild(el('div', { class: 'os-text-sub' }, formatDate(source.last_synced_at)))

          // Dropdown menu
          var menu = el('div', { class: 'os-menu' })
          var menuBtn = el('button', { class: 'os-menu-btn' }, '⋯')
          var dropdown = el('div', { class: 'os-menu-dropdown', style: 'display:none' })

          var editItem = el('div', { class: 'os-menu-item', onClick: function (e) { e.stopPropagation(); dropdown.style.display = 'none'; onEdit(source) } }, '✏ Edit')
          var syncItem = el('div', { class: 'os-menu-item', onClick: function (e) {
            e.stopPropagation(); dropdown.style.display = 'none'
            toast.info('Syncing ' + (source.source_name || source.name) + '...')
            apiCall('order_integration.order_integration.doctype.order_sync_source.order_sync_source.trigger_manual_sync', { source_name: source.name })
              .then(function (result) {
                if (result && result.status === 'success') {
                  var created = (result.leads_created || []).length
                  var skipped = (result.leads_skipped || []).length
                  var errors = (result.leads_errors || []).length
                  toast.success('Sync done: ' + created + ' created, ' + skipped + ' skipped, ' + errors + ' errors')
                } else if (result && result.status === 'error') {
                  toast.error('Sync failed: ' + (result.message || 'Unknown error'))
                } else {
                  toast.success('Sync completed')
                }
              })
              .catch(function (err) {
                toast.error('Sync failed: ' + (err && err.message ? err.message : String(err)))
              })
          }}, '↻ Sync Now')
   var delItem = el('div', {
  class: 'os-menu-item danger',
  onClick: function (e) {
    e.stopPropagation()
    dropdown.style.display = 'none'

    // 🔥 first click
    if (!source._confirm_delete) {
      source._confirm_delete = true

      // store toast id
      source._toast_id = toast.warning(
        'Click Delete again from menu to confirm delete within 10 seconds'
      )

      // reset after 3 sec
      source._timer = setTimeout(function () {
        source._confirm_delete = false

        // auto remove toast if still visible
        if (source._toast_id) {
          toast.dismiss(source._toast_id)
          source._toast_id = null
        }
      }, 10000)

      return
    }

    // ✅ second click → REMOVE toast immediately
    if (source._toast_id) {
      toast.dismiss(source._toast_id)
      source._toast_id = null
    }

    clearTimeout(source._timer)
    source._confirm_delete = false

    // 👉 proceed delete
    apiCall(
      'order_integration.order_integration.doctype.order_sync_source.order_sync_source.delete_order_source',
      { source_name: source.name }
    )
      .then(function () {
        toast.success('Source deleted')
        renderSourcesList(container, onNew, onEdit)
      })
      .catch(function () {
        toast.error('Delete failed')
      })
  }
}, '🗑 Delete')

          dropdown.appendChild(editItem)
          dropdown.appendChild(syncItem)
          dropdown.appendChild(delItem)

          menuBtn.addEventListener('click', function (e) {
            e.stopPropagation()
            var isOpen = dropdown.style.display !== 'none'
            document.querySelectorAll('.os-menu-dropdown').forEach(function (d) { d.style.display = 'none' })
            dropdown.style.display = isOpen ? 'none' : 'block'
          })

          menu.appendChild(menuBtn)
          menu.appendChild(dropdown)
          lastCol.appendChild(menu)
          row.appendChild(lastCol)
          list.appendChild(row)

          if (i < sources.length - 1) {
            list.appendChild(el('div', { class: 'os-divider', style: 'margin:0 4px' }))
          }
        })
        page.appendChild(list)
      }

      container.appendChild(page)
    }).catch(function (e) {
      console.error('[OrderSync] Failed to load sources:', e)
      var errorMsg = e && e.message ? e.message : String(e)
      container.innerHTML = '<div class="os-page"><div style="padding:24px;color:#dc2626"><p>Failed to load sources:</p><p style="font-size:0.85rem;margin-top:8px;font-family:monospace;background:#fef2f2;padding:8px;border-radius:4px">' + errorMsg + '</p></div></div>'
    })

    document.addEventListener('click', function () {
      document.querySelectorAll('.os-menu-dropdown').forEach(function (d) { d.style.display = 'none' })
    }, { once: false, capture: true })
  }

  // ── Source Form view ───────────────────────────────────────────────────────
  function renderSourceForm(container, sourceData, onBack) {
    container.innerHTML = ''
    var isNew = !sourceData || !sourceData.name
    var data = Object.assign({
      name: '', source_name: '', api_key: '',
      sync_frequency: 'Every 5 Minutes', access_token: '', api_url: '',
    }, sourceData || {})

    var page = el('div', { class: 'os-page' })

    // Header
    var header = el('div', { class: 'os-header' })
    var backBtn = el('button', { class: 'os-btn-back', onClick: onBack })
    backBtn.innerHTML = '← ' + (isNew ? 'New Order Sync Source' : (data.source_name || data.name))
    header.appendChild(backBtn)

    var actions = el('div', { class: 'os-actions' })
    if (!isNew) {
      var syncBtn = btn('Sync Now', 'os-btn-outline', function () {
        syncBtn.disabled = true
        syncBtn.textContent = 'Syncing...'
        apiCall(
          'order_integration.order_integration.doctype.order_sync_source.order_sync_source.trigger_manual_sync',
          { source_name: data.name }
        ).then(function (result) {
          syncBtn.disabled = false
          syncBtn.textContent = 'Sync Now'
          if (result && result.status === 'success') {
            var created = (result.leads_created || []).length
            var skipped = (result.leads_skipped || []).length
            var errors = (result.leads_errors || []).length
            toast.success('Sync done: ' + created + ' created, ' + skipped + ' skipped, ' + errors + ' errors')
          } else if (result && result.status === 'error') {
            toast.error('Sync failed: ' + (result.message || 'Unknown error'))
          } else {
            toast.success('Sync completed')
          }
        }).catch(function (err) {
          syncBtn.disabled = false
          syncBtn.textContent = 'Sync Now'
          toast.error('Sync failed: ' + (err && err.message ? err.message : String(err)))
        })
      }, '↻')
      actions.appendChild(syncBtn)
    }

    var saveBtn = btn(isNew ? 'Create' : 'Update', 'os-btn-solid', doSave)
    actions.appendChild(saveBtn)
    header.appendChild(actions)
    page.appendChild(header)

    // Form fields
    var form = el('div', { class: 'os-form' })

    function field(label, inputEl, fullWidth) {
      var wrap = el('div', { class: 'os-field' + (fullWidth ? ' os-form-full' : '') })
      wrap.appendChild(el('label', { class: 'os-label' }, label))
      wrap.appendChild(inputEl)
      return wrap
    }

    var nameInput = el('input', { class: 'os-input', type: 'text', placeholder: 'e.g. My Store', value: data.source_name })
    var apiKeyInput = el('input', { class: 'os-input', type: 'text', placeholder: 'e.g. ipshopy', value: data.api_key || '' })
    var freqSelect = el('select', { class: 'os-select' })
    ;['Every 5 Minutes', 'Every 10 Minutes', 'Hourly', 'Daily'].forEach(function (opt) {
      var o = el('option', { value: opt }, opt)
      if (opt === data.sync_frequency) o.selected = true
      freqSelect.appendChild(o)
    })

    var sourceTypeSelect = el('select', { class: 'os-select' })
    ;[
      { value: '', label: '— Select Source Type —' },
      { value: 'cart_data', label: ' Customer Side' },
      { value: 'ticket_data', label: 'Seller Side' },
      { value: 'both', label: 'Both' },
    ].forEach(function (opt) {
      var o = el('option', { value: opt.value }, opt.label)
      if (opt.value === (data.source_type || '')) o.selected = true
      sourceTypeSelect.appendChild(o)
    })

    // For edit mode, leave blank
    var tokenPlaceholder = isNew ? 'Enter access token' : 'Leave blank to keep existing'
    var tokenInput = el('input', { class: 'os-input', type: 'password', placeholder: tokenPlaceholder, value: '' })
    var urlInput = el('input', { class: 'os-input', type: 'text', placeholder: 'https://api.yourstore.com', value: data.api_url || '' })

    form.appendChild(field('Source Name *', nameInput))
    form.appendChild(field('API Key', apiKeyInput))
    form.appendChild(field('Sync Frequency *', freqSelect))
    form.appendChild(field('Source Type *', sourceTypeSelect))
    form.appendChild(field('Access Token' + (isNew ? ' *' : ''), tokenInput))
    form.appendChild(field('API URL *', urlInput, true))

    // Test Connection button
    var testBtn = btn('Test Connection', 'os-btn-outline', function () {
      var url = urlInput.value.trim()
      var token = tokenInput.value || ''

      if (!url) {
        toast.error('Please enter API URL first')
        return
      }
      if (!token && !data.has_access_token) {
        toast.error('Please enter Access Token first')
        return
      }

      testBtn.disabled = true
      testBtn.textContent = 'Testing...'

      apiCall(
        'order_integration.order_integration.doctype.order_sync_source.order_sync_source.test_api_connection',
        { api_url: url, access_token: token, api_key: apiKeyInput.value.trim(), source_name: data.name || '' }
      ).then(function (result) {
        testBtn.disabled = false
        testBtn.textContent = 'Test Connection'

        if (result.status === 'success') {
          toast.success(result.message)
        } else if (result.status === 'warning') {
          toast.warning(result.message)
        } else {
          toast.error(result.message || 'Connection test failed')
        }
      }).catch(function (err) {
        testBtn.disabled = false
        testBtn.textContent = 'Test Connection'
        toast.error('Error: ' + (err.message || 'Connection test failed'))
      })
    })

    var testField = el('div', { class: 'os-field os-form-full' })
    testField.appendChild(testBtn)
    form.appendChild(testField)

    if (!isNew && data.last_synced_at) {
      form.appendChild(el('div', { class: 'os-form-full os-text-sub' }, 'Last synced: ' + formatDate(data.last_synced_at)))
    }

    page.appendChild(form)
    container.appendChild(page)

    function doSave() {
      var doc = {
        name: data.name,
        source_name: nameInput.value.trim(),
        api_key: apiKeyInput.value.trim(),
        sync_frequency: freqSelect.value,
        source_type: sourceTypeSelect.value,
        access_token: tokenInput.value,
        api_url: urlInput.value.trim(),
      }
      if (!doc.source_name || !doc.api_url) {
        toast.error('Please fill in all required fields')
        return
      }
      if (!doc.source_type) {
        toast.error('Please select a Source Type')
        return
      }
      // For new sources, access token is required
      // For edit, if empty, it means keep existing (backend will handle this)
      if (isNew && !doc.access_token) {
        toast.error('Access token is required')
        return
      }
      saveBtn.disabled = true
      saveBtn.textContent = 'Saving...'

      // Pass doc as JSON string to match backend expectation
      apiCall(
        'order_integration.order_integration.doctype.order_sync_source.order_sync_source.save_order_source',
        { doc: JSON.stringify(doc), is_edit: !isNew }
      ).then(function (result) {
        // Check if the result is an error response
        if (result && result.status === 'error') {
          toast.error(result.message || 'Error saving source')
          saveBtn.disabled = false
          saveBtn.textContent = isNew ? 'Create' : 'Update'
          return
        }

        // Check if result is success
        if (result && (result.status === 'success' || result.name)) {
          toast.success(isNew ? 'Source created' : 'Source updated')
          onBack()
          return
        }

        // If we get here, something unexpected happened
        toast.success(isNew ? 'Source created' : 'Source updated')
        onBack()
      }).catch(function (e) {
        var errorMsg = 'Error saving source'

        // Try to extract the actual error message from various error formats
        if (e && e.message) {
          errorMsg = e.message
        } else if (e && typeof e === 'string') {
          errorMsg = e
        } else if (e && e.exc) {
          errorMsg = e.exc
        } else if (e && e._server_messages) {
          try {
            var msgs = JSON.parse(e._server_messages)
            if (msgs && msgs.length > 0) {
              errorMsg = msgs[0]
            }
          } catch (parseErr) {}
        }

        toast.error(errorMsg)
        saveBtn.disabled = false
        saveBtn.textContent = isNew ? 'Create' : 'Update'
      })
    }
  }

  // ── Main mount function ────────────────────────────────────────────────────
  window.__OrderSyncMount = function (mountEl) {
    injectStyles()

    function showList() {
      renderSourcesList(mountEl, showNewForm, function (source) {
        showEditForm(source)
      })
    }

    function showNewForm() {
      renderSourceForm(mountEl, null, showList)
    }

    function showEditForm(source) {
      renderSourceForm(mountEl, source, showList)
    }

    showList()
  }
})()
