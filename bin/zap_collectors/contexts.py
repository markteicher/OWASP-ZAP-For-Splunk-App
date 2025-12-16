# zap_collectors/contexts.py

def collect_contexts(zap_client):
    """
    Collect context definitions from ZAP.

    :param zap_client: initialized ZAP API client
    :return: list of context records
    """

    records = []

    # Get list of context names
    response = zap_client.get(
        "/JSON/context/view/contextList/"
    )

    context_names = response.get("contextList", [])

    for name in context_names:
        # Get full context details
        context_detail = zap_client.get(
            "/JSON/context/view/context/",
            params={"contextName": name}
        )

        records.append({
            "context_name": name,
            "context": context_detail.get("context", {})
        })

    return records
