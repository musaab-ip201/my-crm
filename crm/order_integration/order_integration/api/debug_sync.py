import frappe


@frappe.whitelist()
def run_debug_sync():
    """Debug endpoint — call from bench console to diagnose sync issues."""
    output = []

    # 1. List all sources
    sources = frappe.get_all(
        "Order Sync Source",
        fields=["name", "source_name", "api_url", "source_type", "sync_frequency"],
    )
    output.append(f"Found {len(sources)} source(s):")
    for s in sources:
        output.append(f"  {s.name} | {s.source_name} | type={s.source_type} | url={s.api_url}")

    if not sources:
        output.append("ERROR: No Order Sync Sources configured!")
        return "\n".join(output)

    # 2. Try to fetch token for first source
    source_name = sources[0].name
    source = frappe.get_doc("Order Sync Source", source_name)

    token = None
    try:
        token = source.get_password("access_token")
    except Exception as e:
        output.append(f"get_password error: {e}")

    if not token:
        token = source.access_token
    output.append(f"Token present: {bool(token)} (length={len(token) if token else 0})")

    # 3. Run sync
    frappe.set_user("Administrator")
    from order_integration.order_integration.doctype.order_sync_source.order_sync_source import sync_orders_now
    result = sync_orders_now(source_name)
    output.append(f"Sync result: {result}")

    # 4. Recent error logs
    logs = frappe.get_all(
        "Error Log",
        fields=["title", "error", "creation"],
        order_by="creation desc",
        limit=5,
    )
    output.append(f"\nRecent error logs ({len(logs)}):")
    for l in logs:
        output.append(f"  [{l.creation}] {l.title}")
        if l.error:
            output.append(f"    {l.error[:400]}")

    return "\n".join(output)
