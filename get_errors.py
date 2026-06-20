import sys, os
sys.path.insert(0, '../../apps/frappe')
import frappe
frappe.init(site='ipshopy-crm')
frappe.connect()
errors = frappe.get_all("Error Log", fields=["method", "error"], limit=3, order_by="creation desc")
for e in errors:
    print("---", e.method, "---")
    print(e.error)
