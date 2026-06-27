"""
Dynamic Lead Ingestion API
Handles flexible API response parsing, schema detection, and dynamic lead creation
"""

import frappe
from frappe import _
import requests
import json
from typing import Dict, List, Any, Tuple


class DynamicLeadIngestion:
    """Handles dynamic lead ingestion from various API sources"""
    
    # Common field mappings for auto-detection
    FIELD_MAPPINGS = {
        'name_fields': ['name', 'customer_name', 'customer', 'full_name', 'title'],
        'email_fields': ['email', 'customer_email', 'email_address'],
        'phone_fields': ['phone', 'mobile', 'mobile_no', 'telephone', 'contact_number'],
        'id_fields': ['id', 'order_id', 'cart_id', 'customer_id', 'reference_id'],
        'status_fields': ['status', 'order_status', 'state', 'stage']
    }
    
    @staticmethod
    def detect_schema(api_response: List[Dict]) -> Dict[str, str]:
        """
        Auto-detect schema from API response
        Returns mapping of detected fields to their types
        """
        if not api_response or len(api_response) == 0:
            return {}
        
        # Get first record as sample
        sample = api_response[0]
        schema = {}
        
        for key, value in sample.items():
            # Determine field type
            if isinstance(value, str):
                field_type = 'string'
            elif isinstance(value, (int, float)):
                field_type = 'number'
            elif isinstance(value, bool):
                field_type = 'boolean'
            elif isinstance(value, dict):
                field_type = 'object'
            elif isinstance(value, list):
                field_type = 'array'
            else:
                field_type = 'unknown'
            
            schema[key] = field_type
        
        return schema
    
    @staticmethod
    def auto_map_fields(api_response: List[Dict]) -> Dict[str, str]:
        """
        Auto-detect and map API fields to CRM Lead fields
        Returns: {crm_field: api_field}
        """
        if not api_response or len(api_response) == 0:
            return {}
        
        sample = api_response[0]
        api_keys = set(sample.keys())
        mapping = {}
        
        # Map name field
        for name_field in DynamicLeadIngestion.FIELD_MAPPINGS['name_fields']:
            if name_field in api_keys:
                mapping['lead_name'] = name_field
                break
        
        # Map email field
        for email_field in DynamicLeadIngestion.FIELD_MAPPINGS['email_fields']:
            if email_field in api_keys:
                mapping['email'] = email_field
                break
        
        # Map phone field
        for phone_field in DynamicLeadIngestion.FIELD_MAPPINGS['phone_fields']:
            if phone_field in api_keys:
                mapping['mobile_no'] = phone_field
                break
        
        # Map status field
        for status_field in DynamicLeadIngestion.FIELD_MAPPINGS['status_fields']:
            if status_field in api_keys:
                mapping['order_status'] = status_field
                break
        
        # Map ID field
        for id_field in DynamicLeadIngestion.FIELD_MAPPINGS['id_fields']:
            if id_field in api_keys:
                mapping['order_id'] = id_field
                break
        
        return mapping
    
    @staticmethod
    def extract_displayable_fields(api_response: List[Dict], max_fields: int = 15) -> List[str]:
        """
        Extract key displayable fields from API response
        Prioritizes: ID, Name, Email, Phone, Status, Subject, Description, then others
        """
        if not api_response or len(api_response) == 0:
            return []
        
        sample = api_response[0]
        priority_fields = []
        other_fields = []
        
        # Priority order - increased to include more important fields
        priority_order = [
            'id', 'order_id', 'cart_id', 'ticket_id', 'customer_id',
            'name', 'customer_name', 'full_name',
            'email', 'customer_email',
            'phone', 'mobile', 'mobile_no', 'telephone',
            'status', 'order_status',
            'subject', 'title',
            'description', 'message',
            'category',
            'created_at', 'created', 'date', 'date_added'
        ]
        
        for field in priority_order:
            if field in sample:
                priority_fields.append(field)
        
        # Add remaining fields
        for field in sample.keys():
            if field not in priority_fields and len(priority_fields) + len(other_fields) < max_fields:
                other_fields.append(field)
        
        return priority_fields + other_fields[:max_fields - len(priority_fields)]
    
    @staticmethod
    def parse_api_response(response_data: Any) -> Tuple[List[Dict], bool]:
        """
        Parse API response and extract records
        Returns: (records_list, is_paginated)
        """
        records = []
        is_paginated = False
        
        if isinstance(response_data, list):
            records = response_data
        elif isinstance(response_data, dict):
            # Try common pagination/data wrapper keys
            wrapper_keys = ['data', 'records', 'items', 'results', 'orders', 'leads', 'customers']
            for key in wrapper_keys:
                if key in response_data and isinstance(response_data[key], list):
                    records = response_data[key]
                    is_paginated = 'total' in response_data or 'total_pages' in response_data
                    break
            
            # If no wrapper found, treat dict as single record
            if not records:
                records = [response_data]
        
        return records, is_paginated


@frappe.whitelist()
def fetch_api_data(source_name: str, page: int = 1, page_size: int = 20) -> Dict:
    """
    Fetch data from API source with dynamic schema detection
    """
    try:
        source = frappe.get_doc("Order Sync Source", source_name)
        access_token = source.get_password("access_token")
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # Add pagination params if supported
        params = {
            'page': page,
            'limit': page_size
        }
        
        response = requests.get(
            source.api_url,
            headers=headers,
            params=params,
            timeout=60,
            verify=True
        )
        
        if response.status_code != 200:
            return {
                "status": "error",
                "message": f"API returned HTTP {response.status_code}"
            }
        
        data = response.json()
        records, is_paginated = DynamicLeadIngestion.parse_api_response(data)
        
        # Detect schema and auto-map fields
        schema = DynamicLeadIngestion.detect_schema(records)
        field_mapping = DynamicLeadIngestion.auto_map_fields(records)
        displayable_fields = DynamicLeadIngestion.extract_displayable_fields(records)
        
        return {
            "status": "success",
            "records": records,
            "schema": schema,
            "field_mapping": field_mapping,
            "displayable_fields": displayable_fields,
            "is_paginated": is_paginated,
            "total_records": len(records),
            "page": page,
            "page_size": page_size
        }
        
    except Exception as e:
        frappe.log_error(f"Error fetching API data: {str(e)}", "Dynamic Lead API")
        return {
            "status": "error",
            "message": str(e)
        }


@frappe.whitelist()
def get_api_sources_for_filter() -> List[Dict]:
    """
    Get all API sources for filter dropdown in Lead View
    """
    try:
        sources = frappe.get_all(
            "Order Sync Source",
            fields=["name", "source_name", "source_type"],
            order_by="source_name asc"
        )
        return sources
    except Exception as e:
        frappe.log_error(f"Error fetching sources: {str(e)}", "Dynamic Lead API")
        return []


@frappe.whitelist()
def create_leads_from_api_data(source_name: str, records: List[Dict], field_mapping: Dict) -> Dict:
    """
    Create CRM Leads from API records using provided field mapping
    """
    try:
        created_leads = []
        failed_records = []
        
        for idx, record in enumerate(records):
            try:
                # Extract mapped fields
                lead_name_val = record.get(field_mapping.get('lead_name', 'name'), 'Unknown')
                email_val = record.get(field_mapping.get('email', 'email'), '').strip()
                phone_val = record.get(field_mapping.get('mobile_no', 'phone'), '').strip()
                status_val = record.get(field_mapping.get('order_status', 'status'), 'New')
                order_id_val = record.get(field_mapping.get('order_id', 'id'), '')
                
                # Validate: at least email or phone required
                if not email_val and not phone_val:
                    failed_records.append({
                        "index": idx,
                        "reason": "No email or phone provided"
                    })
                    continue
                
                # Normalize phone
                if phone_val:
                    phone_val = ''.join(filter(str.isdigit, phone_val))
                
                # Check for duplicates
                if email_val and frappe.db.exists("CRM Lead", {"email": email_val}):
                    failed_records.append({
                        "index": idx,
                        "reason": f"Lead with email {email_val} already exists"
                    })
                    continue
                
                # Create lead
                lead_doc = frappe.get_doc({
                    "doctype": "CRM Lead",
                    "lead_name": lead_name_val,
                    "email": email_val if email_val else None,
                    "mobile_no": phone_val if phone_val else None,
                    "status": status_val if status_val else "New",
                    "order_status": status_val,
                    "order_id": order_id_val
                })
                
                lead_doc.insert(ignore_permissions=True)
                frappe.db.commit()
                
                created_leads.append({
                    "name": lead_doc.name,
                    "lead_name": lead_name_val,
                    "email": email_val
                })
                
            except Exception as e:
                failed_records.append({
                    "index": idx,
                    "reason": str(e)
                })
        
        return {
            "status": "success",
            "created": len(created_leads),
            "failed": len(failed_records),
            "created_leads": created_leads,
            "failed_records": failed_records
        }
        
    except Exception as e:
        frappe.log_error(f"Error creating leads: {str(e)}", "Dynamic Lead API")
        return {
            "status": "error",
            "message": str(e)
        }


print("[ORDER_INTEGRATION] ✅ dynamic_lead_api.py loaded")
