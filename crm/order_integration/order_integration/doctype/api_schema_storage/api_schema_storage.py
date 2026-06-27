import json

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.model.document import Document


class APISchemaStorage(Document):
    """Stores the flattened column list detected from an API response."""
    pass


# ─────────────────────────────────────────────────────────────────────────────
# Schema detection
# ─────────────────────────────────────────────────────────────────────────────

def flatten_record(record, prefix="", separator="."):
    """
    Recursively flatten a nested dict into dot-notation keys.

    Example input:
        {"ticket_id": 1, "customer": {"id": 5, "name": "Alice"}}
    Example output:
        {"ticket_id": 1, "customer.id": 5, "customer.name": "Alice"}

    Lists are stored as JSON strings (not further expanded).
    """
    result = {}
    for key, value in record.items():
        full_key = f"{prefix}{separator}{key}" if prefix else key
        if isinstance(value, dict):
            result.update(flatten_record(value, prefix=full_key, separator=separator))
        else:
            # Lists and primitives stored as-is
            result[full_key] = value
    return result


def detect_columns_from_records(records):
    """
    Walk through up to 20 records and collect every unique flattened key.
    Returns a stable list of column names (dot-notation for nested fields).
    """
    seen = {}
    for record in records[:20]:
        if not isinstance(record, dict):
            continue
        flat = flatten_record(record)
        for key in flat:
            if key not in seen:
                seen[key] = True
    return list(seen.keys())


# ─────────────────────────────────────────────────────────────────────────────
# Custom field management
# ─────────────────────────────────────────────────────────────────────────────

def _safe_fieldname(source_name, col):
    """
    Build a valid Frappe fieldname from source_name + column key.
    Replaces dots, spaces, hyphens with underscores and lowercases everything.
    Max 140 chars (Frappe limit).
    """
    import re
    src = re.sub(r"[^a-z0-9_]", "_", source_name.lower())
    col_clean = re.sub(r"[^a-z0-9_]", "_", col.lower())
    name = f"api_col_{src}_{col_clean}"
    return name[:140]


def _human_label(source_label, col):
    """Turn 'customer.name' → 'Customer Name' and prefix with source label."""
    parts = col.replace(".", " ").replace("_", " ").title()
    return f"{source_label}: {parts}"


def ensure_custom_fields_for_source(source_name, columns):
    """
    Create any missing custom fields on CRM Lead for the given columns.
    Idempotent — safe to call multiple times.
    """
    if not columns:
        return

    try:
        source = frappe.get_doc("Order Sync Source", source_name)
        source_label = source.source_name or source_name
    except Exception:
        source_label = source_name

    fields_to_create = []
    for col in columns:
        fieldname = _safe_fieldname(source_name, col)
        cf_name = f"CRM Lead-{fieldname}"
        if frappe.db.exists("Custom Field", cf_name):
            continue
        fields_to_create.append(
            {
                "fieldname": fieldname,
                "fieldtype": "Data",
                "label": _human_label(source_label, col),
                "insert_after": "order_source",
                "in_list_view": 0,
                "in_standard_filter": 0,
                "search_index": 0,
                "reqd": 0,
                "read_only": 1,
                # Metadata: which source owns this field
                "description": f"api_source:{source_name}",
            }
        )

    if fields_to_create:
        create_custom_fields({"CRM Lead": fields_to_create})
        frappe.db.commit()


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

@frappe.whitelist()
def save_api_schema(source_name, schema_fields, columns):
    """
    Persist the detected schema and create custom fields.
    Called after a successful API fetch.
    """
    try:
        if isinstance(schema_fields, str):
            schema_fields = json.loads(schema_fields)
        if isinstance(columns, str):
            columns = json.loads(columns)

        existing = frappe.db.exists("API Schema Storage", {"order_source": source_name})
        if existing:
            doc = frappe.get_doc("API Schema Storage", existing)
        else:
            doc = frappe.new_doc("API Schema Storage")
            doc.order_source = source_name

        doc.schema_fields = json.dumps(schema_fields)
        doc.columns = json.dumps(columns)
        doc.save(ignore_permissions=True)
        frappe.db.commit()

        # Create custom fields immediately
        ensure_custom_fields_for_source(source_name, columns)

        return {"status": "success", "message": "Schema saved", "columns": columns}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "API Schema Storage Error")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def get_api_schema(source_name):
    """Return stored columns for a source."""
    try:
        doc = frappe.get_doc("API Schema Storage", {"order_source": source_name})
        columns = json.loads(doc.columns or "[]")
        return {"status": "success", "columns": columns}
    except frappe.DoesNotExistError:
        return {"status": "not_found", "columns": []}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "API Schema Storage Error")
        return {"status": "error", "columns": []}


@frappe.whitelist()
def get_columns_for_source(source_name):
    """
    Return the custom fields that belong to a specific Order Sync Source.
    Used by the frontend to filter the 'Add Column' dropdown.
    """
    try:
        if not source_name:
            return {"status": "success", "fields": []}

        fields = frappe.get_all(
            "Custom Field",
            filters={
                "dt": "CRM Lead",
                "fieldname": ["like", "api_col_%"],
                "description": ["like", f"api_source:{source_name}%"],
            },
            fields=["fieldname", "label", "fieldtype"],
            order_by="label asc",
        )
        return {"status": "success", "fields": fields}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Column Filter Error")
        return {"status": "error", "fields": []}


@frappe.whitelist()
def get_all_source_field_map():
    """
    Return {fieldname: source_name} for every api_col_* field.
    Used by the frontend to hide irrelevant columns when a source filter is active.
    """
    try:
        fields = frappe.get_all(
            "Custom Field",
            filters={"dt": "CRM Lead", "fieldname": ["like", "api_col_%"]},
            fields=["fieldname", "description"],
        )
        field_map = {}
        for f in fields:
            desc = f.get("description") or ""
            if "api_source:" in desc:
                source = desc.split("api_source:")[1].strip()
                field_map[f["fieldname"]] = source
        return {"status": "success", "field_map": field_map}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Column Filter Error")
        return {"status": "error", "field_map": {}}
