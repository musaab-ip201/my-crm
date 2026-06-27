/**
 * Order Syncing — Settings Sidebar Injector
 *
 * Injects "Order Syncing" below "Lead Syncing" in the CRM Settings sidebar.
 * On click, mounts the Order Syncing UI (from order_sync_components.js) into
 * the settings right panel — identical UX to Lead Syncing.
 *
 * Scoped to order.localhost only. No CRM source files modified.
 */
;(function () {
  'use strict'

  var ITEM_ID = 'order-syncing-sidebar-item'
  var PANEL_ID = 'order-syncing-panel-mount'

  // ── Site guard ─────────────────────────────────────────────────────────────
  function isSiteAllowed() {
    // Allow all sites
    return true
  }

  // ── Cart SVG icon ──────────────────────────────────────────────────────────
  var CART_SVG =
    '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" ' +
    'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
    'stroke-linecap="round" stroke-linejoin="round" class="size-4 text-ink-gray-7">' +
    '<circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle>' +
    '<path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>' +
    '</svg>'

  // ── Find "Lead Syncing" button ─────────────────────────────────────────────
  function findLeadSyncingButton() {
    var buttons = document.querySelectorAll('button')
    for (var i = 0; i < buttons.length; i++) {
      var spans = buttons[i].querySelectorAll('span')
      for (var j = 0; j < spans.length; j++) {
        if (spans[j].textContent.trim() === 'Lead Syncing') return buttons[i]
      }
    }
    return null
  }

  // ── Find the settings right panel ─────────────────────────────────────────
  // Settings.vue: sidebar is .w-52.shrink-0.bg-surface-gray-2,
  //               right panel is its next sibling
  function findRightPanel() {
    var sidebar = document.querySelector('.w-52.shrink-0.bg-surface-gray-2')
    return sidebar ? sidebar.nextElementSibling : null
  }

  // ── Remove the panel overlay ───────────────────────────────────────────────
  function removePanel() {
    var old = document.getElementById(PANEL_ID)
    if (old) {
      if (old.parentElement && old.parentElement._osOrigPos !== undefined) {
        old.parentElement.style.position = old.parentElement._osOrigPos
        delete old.parentElement._osOrigPos
      }
      old.remove()
    }
  }

  // ── Mount Order Syncing UI into the right panel ────────────────────────────
  function mountPanel() {
    var rightPanel = findRightPanel()
    if (!rightPanel) return

    removePanel()

    var mountEl = document.createElement('div')
    mountEl.id = PANEL_ID
    mountEl.style.cssText =
      'position:absolute;inset:0;z-index:10;overflow-y:auto;' +
      'background:var(--surface-modal)'

    if (rightPanel._osOrigPos === undefined) {
      rightPanel._osOrigPos = rightPanel.style.position || ''
    }
    rightPanel.style.position = 'relative'
    rightPanel.appendChild(mountEl)

    if (typeof window.__OrderSyncMount === 'function') {
      window.__OrderSyncMount(mountEl)
    } else {
      // Shouldn't happen — order_sync_components.js loads before this script
      mountEl.innerHTML = '<div style="padding:24px;color:#dc2626">Order Syncing failed to load.</div>'
    }
  }

  // ── Deactivate all sidebar buttons visually and close panel ────────────────
  function deactivateAll() {
    var sidebar = document.querySelector('.w-52.shrink-0.bg-surface-gray-2')
    if (!sidebar) return
    sidebar.querySelectorAll('button').forEach(function (b) {
      b.classList.remove('bg-surface-selected', 'shadow-sm')
    })
    removePanel()
  }

  // ── Build the injected sidebar button ──────────────────────────────────────
  function buildItem(leadBtn) {
    var btn = leadBtn.cloneNode(true)
    btn.id = ITEM_ID
    btn.className = btn.className
      .replace(/bg-surface-selected/g, '')
      .replace(/shadow-sm/g, '')
      .trim()

    // Update label
    btn.querySelectorAll('span').forEach(function (s) {
      if (s.textContent.trim() === 'Lead Syncing') s.textContent = 'Order Syncing'
    })

    // Swap icon
    var iconWrap = btn.querySelector('span.grid')
    if (iconWrap) iconWrap.innerHTML = CART_SVG
    else {
      var svg = btn.querySelector('svg')
      if (svg) {
        var tmp = document.createElement('span')
        tmp.innerHTML = CART_SVG
        svg.parentNode.replaceChild(tmp.firstChild, svg)
      }
    }

    // Strip Vue listeners via re-clone, then attach ours
    var clean = btn.cloneNode(true)
    clean.id = ITEM_ID
    clean.addEventListener('click', function (e) {
      e.preventDefault()
      e.stopPropagation()
      deactivateAll()
      clean.classList.add('bg-surface-selected', 'shadow-sm')
      mountPanel()
    })
    
    // Add click listeners to other sidebar buttons to close the panel
    setTimeout(function () {
      var sidebar = document.querySelector('.w-52.shrink-0.bg-surface-gray-2')
      if (sidebar) {
        sidebar.querySelectorAll('button').forEach(function (b) {
          if (b.id !== ITEM_ID && !b.hasAttribute('data-os-listener')) {
            b.setAttribute('data-os-listener', 'true')
            b.addEventListener('click', function () {
              removePanel()
            })
          }
        })
      }
    }, 100)
    
    return clean
  }

  // ── Inject item after Lead Syncing ─────────────────────────────────────────
  function tryInject() {
    var stale = document.getElementById(ITEM_ID)
    if (stale) stale.remove()

    var leadBtn = findLeadSyncingButton()
    if (!leadBtn) return false

    leadBtn.parentNode.insertBefore(buildItem(leadBtn), leadBtn.nextSibling)
    return true
  }

  // ── MutationObserver ───────────────────────────────────────────────────────
  function startObserver() {
    var timer = null
    var observer = new MutationObserver(function (mutations) {
      for (var i = 0; i < mutations.length; i++) {
        var m = mutations[i]

        // Modal closed — clean up panel
        if (m.removedNodes.length) {
          for (var r = 0; r < m.removedNodes.length; r++) {
            var node = m.removedNodes[r]
            if (node.nodeType !== 1) continue
            if (
              (node.classList && node.classList.contains('w-52')) ||
              (node.querySelector && node.querySelector('.w-52.shrink-0'))
            ) removePanel()
          }
        }

        // DOM added — re-inject if needed
        if (m.addedNodes.length) {
          clearTimeout(timer)
          timer = setTimeout(function () {
            if (!document.getElementById(ITEM_ID) && findLeadSyncingButton()) tryInject()
          }, 120)
        }
      }
    })
    observer.observe(document.body, { childList: true, subtree: true })
  }

  // ── Bootstrap ──────────────────────────────────────────────────────────────
  function init() {
    if (!isSiteAllowed()) return
    startObserver()
    setTimeout(tryInject, 300)
  }

  function waitForBoot() {
    if (typeof frappe !== 'undefined' && frappe.boot) { init(); return }
    var n = 0
    var t = setInterval(function () {
      if (typeof frappe !== 'undefined' && frappe.boot) { clearInterval(t); init() }
      else if (++n > 60) { clearInterval(t); init() }
    }, 200)
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', waitForBoot)
  else waitForBoot()
})()
