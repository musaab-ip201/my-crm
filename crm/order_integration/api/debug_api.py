"""
Debug API - For troubleshooting column filtering and data population
"""

import frappe


@frappe.whitelist()
def get_custom_fields_for_lead():
    """Get all custom fields on CRM Lead"""
    try:
        fields = frappe.get_all(
            "Custom Field",
            filters={"dt": "CRM Lead"},
            fields=["fieldname", "label", "description", "in_list_view", "read_only"],
            order_by="fieldname asc"
        )
        
        # Filter to show API columns
        api_fields = [f for f in fields if f['fieldname'].startswith('api_col_')]
        
        return {
            "status": "success",
            "total_fields": len(fields),
            "api_fields_count": len(api_fields),
            "api_fields": api_fields
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@frappe.whitelist()
def get_lead_data(lead_name):
    """Get all data for a specific lead including API columns"""
    try:
        lead = frappe.get_doc("CRM Lead", lead_name)
        
        # Get all custom fields
        custom_fields = frappe.get_all(
            "Custom Field",
            filters={"dt": "CRM Lead", "fieldname": ["like", "api_col_%"]},
            fields=["fieldname"]
        )
        
        # Build response with all field values
        lead_data = {
            "name": lead.name,
            "lead_name": lead.lead_name,
            "email": lead.email,
            "mobile_no": lead.mobile_no,
            "status": lead.status,
            "order_source": lead.order_source,
            "api_columns": {}
        }
        
        # Get values for all API columns
        for cf in custom_fields:
            fieldname = cf['fieldname']
            try:
                value = lead.get(fieldname)
                lead_data["api_columns"][fieldname] = value
            except:
                lead_data["api_columns"][fieldname] = None
        
        return {
            "status": "success",
            "lead": lead_data
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@frappe.whitelist()
def get_api_schema_storage(source_name):
    """Get stored schema for an API source"""
    try:
        doc = frappe.get_doc("API Schema Storage", {"order_source": source_name})
        
        return {
            "status": "success",
            "source_name": source_name,
            "schema_fields": doc.schema_fields,
            "columns": doc.columns
        }
    except frappe.DoesNotExistError:
        return {
            "status": "not_found",
            "message": f"No schema found for source: {source_name}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@frappe.whitelist()
def test_column_visibility():
    """Test if columns are properly set up for visibility"""
    try:
        # Get all API columns
        api_fields = frappe.get_all(
            "Custom Field",
            filters={"dt": "CRM Lead", "fieldname": ["like", "api_col_%"]},
            fields=["fieldname", "description"]
        )
        
        # Build source map
        source_map = {}
        for field in api_fields:
            if field['description'] and 'api_source:' in field['description']:
                source = field['description'].split('api_source:')[1].strip()
                if source not in source_map:
                    source_map[source] = []
                source_map[source].append(field['fieldname'])
        
        # Get sample leads
        leads = frappe.get_all(
            "CRM Lead",
            filters={"order_source": ["!=", ""]},
            fields=["name", "order_source"],
            limit_page_length=5
        )
        
        # Check if leads have data in API columns
        leads_with_data = []
        for lead in leads:
            lead_doc = frappe.get_doc("CRM Lead", lead['name'])
            api_data = {}
            
            for field in api_fields:
                if field['fieldname'].startswith(f"api_col_{lead['order_source'].lower().replace('-', '_')}"):
                    try:
                        value = lead_doc.get(field['fieldname'])
                        if value:
                            api_data[field['fieldname']] = value
                    except:
                        pass
            
            leads_with_data.append({
                "lead_name": lead['name'],
                "order_source": lead['order_source'],
                "api_data_count": len(api_data),
                "api_data": api_data
            })
        
        return {
            "status": "success",
            "source_map": source_map,
            "leads_sample": leads_with_data
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
