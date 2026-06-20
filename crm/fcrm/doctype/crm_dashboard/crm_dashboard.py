
# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class CRMDashboard(Document):
    pass



def default_manager_dashboard_layout():
    """
    Returns the default layout for the CRM Manager Dashboard.
    """
    # Updated lead_action_insights width to 10 and added lead_status_analytics at the same Y coordinate
    return '[{"name":"total_leads","type":"number_chart","tooltip":"Total number of leads","layout":{"x":0,"y":0,"w":4,"h":3,"i":"total_leads"}},{"name":"ongoing_deals","type":"number_chart","tooltip":"Total number of ongoing deals","layout":{"x":8,"y":0,"w":4,"h":3,"i":"ongoing_deals"}},{"name":"won_deals","type":"number_chart","tooltip":"Total number of won deals","layout":{"x":12,"y":0,"w":4,"h":3,"i":"won_deals"}},{"name":"average_won_deal_value","type":"number_chart","tooltip":"Average value of won deals","layout":{"x":16,"y":0,"w":4,"h":3,"i":"average_won_deal_value"}},{"name":"average_deal_value","type":"number_chart","tooltip":"Average deal value of ongoing and won deals","layout":{"x":0,"y":2,"w":4,"h":3,"i":"average_deal_value"}},{"name":"average_time_to_close_a_lead","type":"number_chart","tooltip":"Average time taken to close a lead","layout":{"x":4,"y":0,"w":4,"h":3,"i":"average_time_to_close_a_lead"}},{"name":"average_time_to_close_a_deal","type":"number_chart","layout":{"x":4,"y":2,"w":4,"h":3,"i":"average_time_to_close_a_deal"}},{"name":"follow_up_leads","type":"number_chart","tooltip":"Total number of leads in Follow Up status","layout":{"x":8,"y":2,"w":4,"h":3,"i":"follow_up_leads"}},{"name":"fresh_leads","type":"number_chart","tooltip":"Leads created today","layout":{"x":12,"y":2,"w":4,"h":3,"i":"fresh_leads"}},{"name":"call_insights","type":"custom","tooltip":"Call center insights and statistics","layout":{"x":0,"y":5,"w":20,"h":8,"minH":8,"i":"call_insights"}},{"name":"followup_insights","type":"custom","tooltip":"Follow-up status tracking","layout":{"x":0,"y":13,"w":20,"h":8,"minH":8,"i":"followup_insights"}},{"name":"call_lifecycle_sunburst","type":"axis_chart","layout":{"x":0,"y":21,"w":10,"h":10,"i":"call_lifecycle_sunburst"}},{"name":"call_volume_data","type":"axis_chart","layout":{"x":10,"y":21,"w":10,"h":10,"i":"call_volume_data"}},{"name":"lead_status_analytics","type":"custom","layout":{"x":0,"y":31,"w":10,"h":10,"i":"lead_status_analytics"}},{"name":"lead_action_insights","type":"custom","layout":{"x":10,"y":31,"w":10,"h":10,"i":"lead_action_insights"}},{"name":"funnel_conversion","type":"axis_chart","layout":{"x":0,"y":41,"w":10,"h":9,"i":"funnel_conversion"}},{"name":"deals_by_stage_donut","type":"donut_chart","layout":{"x":10,"y":41,"w":10,"h":9,"i":"deals_by_stage_donut"}},{"name":"sales_trend","type":"axis_chart","layout":{"x":0,"y":50,"w":10,"h":9,"i":"sales_trend"}},{"name":"forecasted_revenue","type":"axis_chart","layout":{"x":10,"y":50,"w":10,"h":9,"i":"forecasted_revenue"}},{"name":"leads_by_source","type":"donut_chart","layout":{"x":0,"y":59,"w":10,"h":9,"i":"leads_by_source"}},{"name":"deals_by_source","type":"donut_chart","layout":{"x":10,"y":59,"w":10,"h":9,"i":"deals_by_source"}},{"name":"deals_by_territory","type":"axis_chart","layout":{"x":0,"y":68,"w":10,"h":9,"i":"deals_by_territory"}},{"name":"deals_by_salesperson","type":"axis_chart","layout":{"x":10,"y":68,"w":10,"h":9,"i":"deals_by_salesperson"}},{"name":"lost_deal_reasons","type":"axis_chart","layout":{"x":0,"y":77,"w":20,"h":9,"i":"lost_deal_reasons"}}]'


def create_default_manager_dashboard(force=False):
    """
    Creates the default CRM Manager Dashboard if it does not exist.
    """
    if not frappe.db.exists("CRM Dashboard", "Manager Dashboard"):
        doc = frappe.new_doc("CRM Dashboard")
        doc.title = "Manager Dashboard"
        doc.layout = default_manager_dashboard_layout()
        doc.insert(ignore_permissions=True)
    else:
        doc = frappe.get_doc("CRM Dashboard", "Manager Dashboard")
        if force:
            doc.layout = default_manager_dashboard_layout()
            doc.save(ignore_permissions=True)
    return doc.layout






# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
# from frappe import _
# from frappe.model.document import Document


# class CRMDashboard(Document):
#     pass


# def default_manager_dashboard_layout():
#     """
#     Returns the default layout for the CRM Manager Dashboard.
#     """
#     # Merged layout with call_insights, follow_up_leads, and custom cards
#     # Includes: Fresh Leads, Call Insights, Follow-Up Insights
    
#     return '[{"name":"total_leads","type":"number_chart","tooltip":"Total number of leads","layout":{"x":0,"y":0,"w":4,"h":3,"i":"total_leads"}},{"name":"ongoing_deals","type":"number_chart","tooltip":"Total number of ongoing deals","layout":{"x":8,"y":0,"w":4,"h":3,"i":"ongoing_deals"}},{"name":"won_deals","type":"number_chart","tooltip":"Total number of won deals","layout":{"x":12,"y":0,"w":4,"h":3,"i":"won_deals"}},{"name":"average_won_deal_value","type":"number_chart","tooltip":"Average value of won deals","layout":{"x":16,"y":0,"w":4,"h":3,"i":"average_won_deal_value"}},{"name":"average_deal_value","type":"number_chart","tooltip":"Average deal value of ongoing and won deals","layout":{"x":0,"y":2,"w":4,"h":3,"i":"average_deal_value"}},{"name":"average_time_to_close_a_lead","type":"number_chart","tooltip":"Average time taken to close a lead","layout":{"x":4,"y":0,"w":4,"h":3,"i":"average_time_to_close_a_lead"}},{"name":"average_time_to_close_a_deal","type":"number_chart","layout":{"x":4,"y":2,"w":4,"h":3,"i":"average_time_to_close_a_deal"}},{"name":"follow_up_leads","type":"number_chart","tooltip":"Total number of leads in Follow Up status","layout":{"x":8,"y":2,"w":4,"h":3,"i":"follow_up_leads"}},{"name":"fresh_leads","type":"number_chart","tooltip":"Leads created today","layout":{"x":12,"y":2,"w":4,"h":3,"i":"fresh_leads"}},{"name":"call_insights","type":"custom","tooltip":"Call center insights and statistics","layout":{"x":0,"y":5,"w":20,"h":8,"minH":8,"i":"call_insights"}},{"name":"followup_insights","type":"custom","tooltip":"Follow-up status tracking","layout":{"x":0,"y":13,"w":20,"h":8,"minH":8,"i":"followup_insights"}},{"name":"call_lifecycle_sunburst","type":"axis_chart","layout":{"x":0,"y":21,"w":10,"h":10,"i":"call_lifecycle_sunburst"}},{"name":"call_volume_data","type":"axis_chart","layout":{"x":10,"y":21,"w":10,"h":10,"i":"call_volume_data"}},{"name":"funnel_conversion","type":"axis_chart","layout":{"x":0,"y":31,"w":10,"h":9,"i":"funnel_conversion"}},{"name":"deals_by_stage_donut","type":"donut_chart","layout":{"x":10,"y":31,"w":10,"h":9,"i":"deals_by_stage_donut"}},{"name":"sales_trend","type":"axis_chart","layout":{"x":0,"y":40,"w":10,"h":9,"i":"sales_trend"}},{"name":"forecasted_revenue","type":"axis_chart","layout":{"x":10,"y":40,"w":10,"h":9,"i":"forecasted_revenue"}},{"name":"leads_by_source","type":"donut_chart","layout":{"x":0,"y":49,"w":10,"h":9,"i":"leads_by_source"}},{"name":"deals_by_source","type":"donut_chart","layout":{"x":10,"y":49,"w":10,"h":9,"i":"deals_by_source"}},{"name":"deals_by_territory","type":"axis_chart","layout":{"x":0,"y":58,"w":10,"h":9,"i":"deals_by_territory"}},{"name":"deals_by_salesperson","type":"axis_chart","layout":{"x":10,"y":58,"w":10,"h":9,"i":"deals_by_salesperson"}},{"name":"lost_deal_reasons","type":"axis_chart","layout":{"x":0,"y":67,"w":20,"h":9,"i":"lost_deal_reasons"}}]'


# def create_default_manager_dashboard(force=False):
    """
    Creates the default CRM Manager Dashboard if it does not exist.
    """
    if not frappe.db.exists("CRM Dashboard", "Manager Dashboard"):
        doc = frappe.new_doc("CRM Dashboard")
        doc.title = "Manager Dashboard"
        doc.layout = default_manager_dashboard_layout()
        doc.insert(ignore_permissions=True)
    else:
        doc = frappe.get_doc("CRM Dashboard", "Manager Dashboard")
        if force:
            doc.layout = default_manager_dashboard_layout()
            doc.save(ignore_permissions=True)
    return doc.layout