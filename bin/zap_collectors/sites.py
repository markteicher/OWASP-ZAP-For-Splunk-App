# zap_collectors/sites.py

def collect_sites(zap_client):
    """
    Collect sites known to ZAP.

    :param zap_client: initialized ZAP API client
    :return: list of site strings or dicts (API dependent)
    """

    response = zap_client.get(
        "/JSON/core/view/sites/"
    )

    # ZAP returns sites as a list under the "sites" key
    sites = response.get("sites", [])

    records = []

    for site in sites:
        records.append({
            "site": site
        })

    return records
