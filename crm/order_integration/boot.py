import frappe
import os


def inject_script_tag(response, request):
    """
    after_request hook — injects scripts into the /crm HTML page
    Works on any site
    """
    try:

        # Only act on /crm paths
        path = request.path or ""
        if not path.startswith("/crm"):
            return

        # Only modify HTML responses
        content_type = response.content_type or ""
        if "text/html" not in content_type:
            return

        # Get response body
        body = response.get_data(as_text=True)
        if not body or "</body>" not in body:
            return

        # Load scripts from files and inject inline
        current_dir = os.path.dirname(os.path.abspath(__file__))
        components_path = os.path.join(current_dir, "public", "js", "order_sync_components.js")
        injector_path = os.path.join(current_dir, "public", "js", "order_sidebar_injector.js")
        crm_lead_list_path = os.path.join(current_dir, "public", "js", "crm_lead_list.js")
        lead_source_filter_path = os.path.join(current_dir, "public", "js", "lead_source_filter.js")
        lead_source_panel_path = os.path.join(current_dir, "public", "js", "lead_source_panel.js")
        dynamic_columns_path = os.path.join(current_dir, "public", "js", "lead_list_dynamic_columns.js")

        scripts = ""
        
        try:
            if os.path.exists(components_path):
                with open(components_path, "r", encoding="utf-8") as f:
                    scripts += "<script>\n" + f.read() + "\n</script>\n"
        except:
            pass
        
        try:
            if os.path.exists(injector_path):
                with open(injector_path, "r", encoding="utf-8") as f:
                    scripts += "<script>\n" + f.read() + "\n</script>\n"
        except:
            pass
        
        try:
            if os.path.exists(crm_lead_list_path):
                with open(crm_lead_list_path, "r", encoding="utf-8") as f:
                    scripts += "<script>\n" + f.read() + "\n</script>\n"
        except:
            pass
        
        try:
            if os.path.exists(lead_source_filter_path):
                with open(lead_source_filter_path, "r", encoding="utf-8") as f:
                    scripts += "<script>\n" + f.read() + "\n</script>\n"
        except:
            pass

        try:
            if os.path.exists(lead_source_panel_path):
                with open(lead_source_panel_path, "r", encoding="utf-8") as f:
                    scripts += "<script>\n" + f.read() + "\n</script>\n"
        except:
            pass

        try:
            if os.path.exists(dynamic_columns_path):
                with open(dynamic_columns_path, "r", encoding="utf-8") as f:
                    scripts += "<script>\n" + f.read() + "\n</script>\n"
        except:
            pass

        if scripts:
            new_body = body.replace("</body>", scripts + "</body>", 1)
            response.set_data(new_body)

    except Exception:
        # Never break the request
        pass
