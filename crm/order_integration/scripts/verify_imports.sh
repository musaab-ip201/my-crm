#!/bin/bash
cd /mnt/d/frappe/ipshopy-bench
env/bin/python << 'EOF'
import sys
sys.path.insert(0, 'apps/frappe')
sys.path.insert(0, 'apps/order_integration')

# Test correct import path
from order_integration.order_integration.doctype.api_schema_storage.api_schema_storage import (
    detect_columns_from_records,
    ensure_custom_fields_for_source,
    save_api_schema,
    flatten_record,
)
print("api_schema_storage imports OK")

from order_integration.order_integration.doctype.order_sync_source.order_sync_source import (
    _flatten,
    _safe_fieldname,
    _fetch_from_api,
    _create_lead,
    sync_orders_now,
    trigger_manual_sync,
)
print("order_sync_source imports OK")

# Test flatten with sample record
sample = {
    "ticket_id": 575,
    "customer_id": 26981,
    "subject": "i need my order",
    "category": "Order Issues",
    "status": "Pending",
    "date_added": "2026-05-14T22:29:14.000Z",
    "order_id": "#186763",
    "customer": {
        "id": 26981,
        "name": "shashi tarachand chirdiya",
        "email": "renu010591@gmail.com",
        "telephone": "9413376452"
    },
    "associated_products": []
}

flat = _flatten(sample)
print(f"\nFlattened {len(flat)} keys:")
for k, v in flat.items():
    print(f"  {k}: {repr(str(v))[:50]}")

cols = detect_columns_from_records([sample])
print(f"\nDetected {len(cols)} columns: {cols}")
print("\nAll OK - ready to sync")
EOF
