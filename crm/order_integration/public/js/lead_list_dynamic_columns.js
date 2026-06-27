;(function () {
  'use strict';

  if (window.__oiDynColsPatched) return;
  window.__oiDynColsPatched = true;

  /* ─── State ─────────────────────────────────────────────────────────────── */
  var _cols         = [];   // [{field, label}, ...]
  var _rows         = {};   // { leadName: { fieldKey: value } }
  var _pendingInject = false;
  var _observer     = null;
  var _retryTimer   = null;
  var _retryCount   = 0;
  var MAX_RETRIES   = 20;   // 20 × 300ms = 6 seconds max

  /* ─── DOM helpers ───────────────────────────────────────────────────────── */

  function clearDynamic() {
    document.querySelectorAll('.oi-dyn-th, .oi-dyn-td').forEach(function (el) {
      el.remove();
    });
  }

  function hardReset() {
    _cols          = [];
    _rows          = {};
    _pendingInject = false;
    _retryCount    = 0;
    clearTimeout(_retryTimer);
    stopObserver();
    clearDynamic();
  }

  /* ─── Injection ─────────────────────────────────────────────────────────── */

  function tryInject() {
    // If reset happened (source deselected), abort
    if (!_cols.length) {
      _pendingInject = false;
      return;
    }

    var rowEls = document.querySelectorAll('[data-list-row-name]');

    if (!rowEls.length) {
      // DOM not ready — retry
      _retryCount++;
      if (_retryCount <= MAX_RETRIES) {
        clearTimeout(_retryTimer);
        _retryTimer = setTimeout(tryInject, 300);
      } else {
        _pendingInject = false;
      }
      return;
    }

    // Reset retry state — we have rows
    _retryCount    = 0;
    _pendingInject = false;

    // Always wipe stale headers/cells first
    clearDynamic();

    /* ── Header row ── */
    var container = rowEls[0].parentElement;
    if (container) {
      // The header is the first child that is NOT a data row
      var header = null;
      for (var i = 0; i < container.children.length; i++) {
        if (!container.children[i].hasAttribute('data-list-row-name')) {
          header = container.children[i];
          break;
        }
      }
      if (header) {
        _cols.forEach(function (col) {
          var th = document.createElement('div');
          th.className = 'oi-dyn-th';
          th.style.cssText = [
            'display:flex;align-items:center;flex-shrink:0;',
            'min-width:120px;padding:4px 8px;',
            'font-size:11px;font-weight:600;text-transform:uppercase;',
            'color:var(--ink-gray-5,#6b7280);white-space:nowrap;',
          ].join('');
          th.textContent = col.label;
          header.appendChild(th);
        });
      }
    }

    /* ── Data cells ── */
    rowEls.forEach(function (rowEl) {
      var leadName = rowEl.getAttribute('data-list-row-name') || '';
      var rowData  = _rows[leadName] || {};
      _cols.forEach(function (col) {
        var td  = document.createElement('div');
        td.className = 'oi-dyn-td';
        td.style.cssText = [
          'display:flex;align-items:center;flex-shrink:0;',
          'min-width:120px;padding:4px 8px;',
          'font-size:12px;color:var(--ink-gray-8,#1f2937);',
          'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;',
        ].join('');
        var val = (rowData[col.field] != null) ? String(rowData[col.field]) : '—';
        td.textContent = val;
        td.title       = val;
        rowEl.appendChild(td);
      });
    });
  }

  /* ─── Observer: re-inject when Vue re-renders list rows ─────────────────── */

  function startObserver() {
    stopObserver();
    var debounce = null;
    _observer = new MutationObserver(function () {
      if (!_cols.length) return;
      // If Vue wiped our headers, re-inject
      if (document.querySelector('[data-list-row-name]') &&
          !document.querySelector('.oi-dyn-th')) {
        clearTimeout(debounce);
        debounce = setTimeout(tryInject, 100);
      }
    });
    _observer.observe(document.body, { childList: true, subtree: true });
  }

  function stopObserver() {
    if (_observer) { _observer.disconnect(); _observer = null; }
  }

  /* ─── Body parsing ───────────────────────────────────────────────────────── */

  function parseFormEncoded(body) {
    var out = {};
    if (!body || typeof body !== 'string') return out;
    body.split('&').forEach(function (pair) {
      var i = pair.indexOf('=');
      if (i < 0) return;
      var k = decodeURIComponent(pair.slice(0, i).replace(/\+/g, ' '));
      var v = decodeURIComponent(pair.slice(i + 1).replace(/\+/g, ' '));
      out[k] = v;
    });
    return out;
  }

  function isLeadListRequest(url, opts) {
    // Must be one of our two API endpoints
    var isOurUrl = url.includes('crm.api.doc.get_data') ||
                   url.includes('override_get_data.get_data');
    if (!isOurUrl) return false;

    // Body check — frappe-ui sends form-encoded
    var body = (opts && opts.body && typeof opts.body === 'string') ? opts.body : '';
    if (!body) {
      // No body but URL matches — still intercept (handles GET variant)
      return isOurUrl;
    }

    var decoded = decodeURIComponent(body);
    // Fastest checks first
    if (decoded.includes('"CRM Lead"') || decoded.includes('CRM Lead')) return true;

    var form = parseFormEncoded(body);
    if (form.doctype === 'CRM Lead') return true;

    // Last resort: any filters-bearing lead request
    if (form.filters) {
      try {
        var f = JSON.parse(form.filters);
        if (f && typeof f === 'object') return true;
      } catch (e) {}
    }

    return false;
  }

  /* ─── Fetch interceptor ─────────────────────────────────────────────────── */

  var _origFetch = window.fetch;

  window.fetch = async function () {
    var args = arguments;
    var url  = typeof args[0] === 'string' ? args[0] : (args[0] && args[0].url) || '';
    var opts = args[1] || {};

    if (!isLeadListRequest(url, opts)) {
      return _origFetch.apply(this, args);
    }

    // Immediately clear stale columns from any previous source selection.
    // We do NOT call hardReset() here — that would wipe _cols before we
    // know if the new response contains columns. Instead we just clear DOM.
    clearTimeout(_retryTimer);
    _pendingInject = false;
    _retryCount    = 0;
    stopObserver();
    clearDynamic();
    // Keep _cols / _rows from previous call only until new response arrives.

    var response = await _origFetch.apply(this, args);

    // Clone response so caller gets an untouched stream
    response.clone().json().then(function (data) {
      var msg     = data && data.message;
      var dynCols = msg && msg._dynamic_columns;

      if (!dynCols || !dynCols.length) {
        // No source selected or API returned nothing — ensure clean state
        _cols = [];
        _rows = {};
        clearDynamic();
        return;
      }

      // Populate state FIRST, then inject
      _cols = dynCols;
      _rows = {};
      (msg.data || []).forEach(function (row) {
        if (row && row.name) _rows[row.name] = row;
      });

      // Start observer so Vue re-renders are caught, then kick off injection
      startObserver();
      _pendingInject = true;
      _retryCount    = 0;
      tryInject();

    }).catch(function () {
      // If JSON parse fails, clear everything
      _cols = [];
      _rows = {};
      clearDynamic();
    });

    return response;
  };

})();
