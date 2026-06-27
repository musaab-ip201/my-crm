;(function () {
  'use strict';

  var DROPDOWN_ID = 'oi-order-source-dropdown';
  var STYLE_ID    = 'oi-order-source-filter-styles';
  window.__oiCurrentSource = window.__oiCurrentSource || null;
  var isInjecting = false;

  // ── Styles ──────────────────────────────────────────────────────────────────
  function injectStyles() {
    if (document.getElementById(STYLE_ID)) return;
    var s = document.createElement('style');
    s.id = STYLE_ID;
    s.textContent = [
      '#' + DROPDOWN_ID + '{display:inline-flex;align-items:center;gap:6px;margin-right:6px;flex-shrink:0;}',
      '#' + DROPDOWN_ID + ' label{font-size:11px;font-weight:600;color:var(--ink-gray-5,#6b7280);white-space:nowrap;}',
      '#' + DROPDOWN_ID + ' select{',
        'height:28px;padding:0 26px 0 8px;',
        'border:1px solid var(--outline-gray-2,#d1d5db);border-radius:6px;',
        'font-size:12px;font-weight:500;',
        'background:var(--surface-white,#fff);',
        'color:var(--ink-gray-8,#1f2937);',
        'cursor:pointer;outline:none;',
        'appearance:none;-webkit-appearance:none;',
        'background-image:url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'10\' height=\'10\' viewBox=\'0 0 24 24\' fill=\'none\' stroke=\'%236b7280\' stroke-width=\'2.5\'%3E%3Cpolyline points=\'6 9 12 15 18 9\'/%3E%3C/svg%3E");',
        'background-repeat:no-repeat;background-position:right 7px center;',
        'transition:border-color .15s,background-color .15s;',
      '}',
      '#' + DROPDOWN_ID + ' select:focus{border-color:var(--outline-blue-3,#3b82f6);}',
      '#' + DROPDOWN_ID + ' select.oi-active{',
        'border-color:var(--outline-blue-3,#3b82f6);',
        'background-color:var(--surface-blue-1,#eff6ff);',
        'color:var(--ink-blue-4,#2563eb);',
      '}',
    ].join('');
    document.head.appendChild(s);
  }

  // ── Fetch sources ────────────────────────────────────────────────────────────
  function fetchSources(cb) {
    var token = '';
    try {
      document.cookie.split(';').forEach(function (c) {
        c = c.trim();
        if (c.startsWith('csrf_token=')) token = c.slice('csrf_token='.length);
      });
    } catch (e) {}
    
    fetch('/api/method/order_integration.order_integration.api.lead_list_dynamic_columns_api.get_available_data_types', {
      method: 'POST', credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'X-Frappe-CSRF-Token': token },
      body: '{}',
    })
      .then(function (r) { return r.json(); })
      .then(function (d) { cb(d.message || []); })
      .catch(function () { cb([]); });
  }

  // ── Find the frappe-ui list resource in the Vue tree ─────────────────────────
  function findListResource() {
    try {
      var app = document.getElementById('app');
      if (!app || !app.__vue_app__) return null;
      var found = null;

      function walk(vnode, depth) {
        if (!vnode || depth > 35 || found) return;
        var comp = vnode.component;
        if (comp && comp.setupState) {
          var state = comp.setupState;
          var keys = Object.keys(state);
          for (var i = 0; i < keys.length && !found; i++) {
            var raw = state[keys[i]];
            var res = (raw && raw.value && typeof raw.value.reload === 'function') ? raw.value : raw;
            if (res && typeof res.reload === 'function' && res.params && res.params.doctype === 'CRM Lead') {
              found = res;
            }
          }
        }
        if (comp && comp.subTree && !found) walk(comp.subTree, depth + 1);
        var ch = vnode.children;
        if (!ch || found) return;
        if (Array.isArray(ch)) {
          for (var i = 0; i < ch.length && !found; i++) walk(ch[i], depth + 1);
        } else if (typeof ch === 'object') {
          var vals = Object.values(ch);
          for (var i = 0; i < vals.length && !found; i++) {
            if (vals[i] && typeof vals[i] === 'object') walk(vals[i], depth + 1);
          }
        }
      }

      var root = app.__vue_app__._instance;
      if (root && root.subTree) walk(root.subTree, 0);
      return found;
    } catch (e) {
      return null;
    }
  }

  // ── Apply filter and reload ──────────────────────────────────────────────────
  function applyFilter(sourceName) {
    window.__oiCurrentSource = sourceName || null;

    document.querySelectorAll('.oi-dyn-th, .oi-dyn-td').forEach(function (el) {
      el.remove();
    });

    var resource = findListResource();
    if (!resource) {
      setTimeout(function () { applyFilter(sourceName); }, 500);
      return;
    }

    var filters = resource.params.filters;
    if (!filters || typeof filters !== 'object') {
      resource.params.filters = {};
      filters = resource.params.filters;
    }

    if (sourceName) {
      filters.order_source = sourceName;
    } else {
      delete filters.order_source;
    }

    resource.reload();
  }

  // ── Build dropdown ───────────────────────────────────────────────────────────
  function buildDropdown(sources) {
    var wrap = document.createElement('div');
    wrap.id = DROPDOWN_ID;

    var lbl = document.createElement('label');
    lbl.textContent = 'Source:';
    wrap.appendChild(lbl);

    var sel = document.createElement('select');
    var opt0 = document.createElement('option');
    opt0.value = '';
    opt0.textContent = 'All';
    sel.appendChild(opt0);

    sources.forEach(function (src) {
      var opt = document.createElement('option');
      opt.value = src.value;
      opt.textContent = src.label || src.value;
      if (window.__oiCurrentSource === src.value) {
        opt.selected = true;
        sel.classList.add('oi-active');
      }
      sel.appendChild(opt);
    });

    sel.addEventListener('change', function () {
      var val = sel.value || null;
      sel.classList.toggle('oi-active', !!val);
      applyFilter(val);
    });

    wrap.appendChild(sel);
    return wrap;
  }

  // ── Find toolbar ─────────────────────────────────────────────────────────────
  function findToolbar() {
    var buttons = document.querySelectorAll('button');
    for (var i = 0; i < buttons.length; i++) {
      var t = buttons[i].textContent.trim();
      if (t === 'Filters' || t === 'Sort By' || t === 'Group By') {
        var el = buttons[i].parentElement;
        while (el && el !== document.body) {
          if (el.classList && el.className.includes('flex')) return el;
          el = el.parentElement;
        }
      }
    }
    return null;
  }

  // ── Inject dropdown ──────────────────────────────────────────────────────────
  function injectDropdown() {
    if (!window.location.pathname.includes('/crm/leads')) return false;
    if (document.getElementById(DROPDOWN_ID) || isInjecting) return true;

    var toolbar = findToolbar();
    if (!toolbar) return false;

    isInjecting = true;
    fetchSources(function (sources) {
      isInjecting = false;
      if (!sources || !sources.length) return;
      if (document.getElementById(DROPDOWN_ID)) return;
      
      var currentToolbar = findToolbar();
      if (currentToolbar) {
        currentToolbar.insertBefore(buildDropdown(sources), currentToolbar.firstChild);
      }
    });
    return true;
  }

  // ── Navigation watcher ───────────────────────────────────────────────────────
  function watchNavigation() {
    var last = window.location.pathname;
    setInterval(function () {
      var cur = window.location.pathname;
      if (cur === last) return;
      last = cur;
      var old = document.getElementById(DROPDOWN_ID);
      if (old) old.remove();
      window.__oiCurrentSource = null;
      if (cur.includes('/crm/leads')) setTimeout(injectDropdown, 900);
    }, 300);
  }

  // ── MutationObserver ─────────────────────────────────────────────────────────
  function startObserver() {
    var timer = null;
    new MutationObserver(function () {
      if (!window.location.pathname.includes('/crm/leads')) return;
      clearTimeout(timer);
      timer = setTimeout(function () {
        if (!document.getElementById(DROPDOWN_ID)) injectDropdown();
      }, 600);
    }).observe(document.body, { childList: true, subtree: true });
  }

  // ── Bootstrap ────────────────────────────────────────────────────────────────
  function init() {
    injectStyles();
    startObserver();
    watchNavigation();
    if (window.location.pathname.includes('/crm/leads')) setTimeout(injectDropdown, 1500);
  }

  function waitForBoot() {
    if (typeof frappe !== 'undefined' && frappe.boot) { init(); return; }
    var n = 0, t = setInterval(function () {
      if (typeof frappe !== 'undefined' && frappe.boot) { clearInterval(t); init(); }
      else if (++n > 80) { clearInterval(t); init(); }
    }, 200);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', waitForBoot);
  else waitForBoot();
})();