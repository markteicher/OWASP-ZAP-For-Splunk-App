# zap_collectors/alerts.py

def collect_alerts(zap_client, params=None):
    """
    Collect alerts from ZAP.

    :param zap_client: initialized ZAP API client
    :param params: optional dict (baseurl, risk, confidence, etc.)
    :return: list of alert dicts
    """

    if params is None:
        params = {}

    response = zap_client.get(
        "/JSON/core/view/alerts/",
        params=params
    )

    # ZAP always returns alerts under the "alerts" key
    alerts = response.get("alerts", [])

    return alerts
