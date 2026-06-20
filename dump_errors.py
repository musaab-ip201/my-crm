
import sys
sys.path.insert(0, '../../apps/frappe')
import frappe
try:
    frappe.init(site="ipcrm.local")
    frappe.connect()
    errors = frappe.get_all("Error Log", fields=["method", "error"], limit=3, order_by="creation desc")
    for e in errors:
        print("--- Error Log ---")
        print(e.error[:1000])
except Exception as e:
    print("Fail:", e)
finally:
    frappe.destroy()
