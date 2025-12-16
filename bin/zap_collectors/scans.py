# zap_collectors/scans.py

def collect_scans(zap_client):
    """
    Collect spider and active scan status from ZAP.

    :param zap_client: initialized ZAP API client
    :return: list of scan records
    """

    records = []

    # Active Scans
    ascan_response = zap_client.get(
        "/JSON/ascan/view/scans/"
    )

    for scan in ascan_response.get("scans", []):
        records.append({
            "scan_type": "active",
            "scan_id": scan.get("scanId"),
            "status": scan.get("status"),
            "progress": scan.get("progress"),
            "url": scan.get("url"),
            "policy": scan.get("policy"),
            "method": scan.get("method")
        })

    # Spider Scans
    spider_response = zap_client.get(
        "/JSON/spider/view/scans/"
    )

    for scan in spider_response.get("scans", []):
        records.append({
            "scan_type": "spider",
            "scan_id": scan.get("id"),
            "status": scan.get("status"),
            "progress": scan.get("progress"),
            "url": scan.get("url")
        })

    return records
