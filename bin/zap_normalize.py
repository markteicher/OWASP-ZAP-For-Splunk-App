# zap_normalize.py

import copy
import time


def now_epoch():
    return int(time.time())


# ---------- ALERTS ----------

def normalize_alert(alert):
    """
    Normalize a single ZAP alert record.
    """

    record = copy.deepcopy(alert)

    return {
        "event_type": "alert",
        "alert_name": record.get("alert"),
        "risk": record.get("risk"),
        "confidence": record.get("confidence"),
        "plugin_id": record.get("pluginId"),
        "cwe_id": record.get("cweid"),
        "wasc_id": record.get("wascid"),
        "url": record.get("url"),
        "param": record.get("param"),
        "attack": record.get("attack"),
        "evidence": record.get("evidence"),
        "solution": record.get("solution"),
        "reference": record.get("reference"),
        "source": "zaproxy",
        "_raw_zap": record,
        "_time": now_epoch()
    }


# ---------- SITES ----------

def normalize_site(site):
    """
    Normalize a ZAP site record.
    """

    return {
        "event_type": "site",
        "site": site.get("site"),
        "source": "zaproxy",
        "_raw_zap": site,
        "_time": now_epoch()
    }


# ---------- SCANS ----------

def normalize_scan(scan):
    """
    Normalize a ZAP scan record.
    """

    record = copy.deepcopy(scan)

    return {
        "event_type": "scan",
        "scan_type": record.get("scan_type"),
        "scan_id": record.get("scan_id"),
        "status": record.get("status"),
        "progress": record.get("progress"),
        "url": record.get("url"),
        "policy": record.get("policy"),
        "method": record.get("method"),
        "source": "zaproxy",
        "_raw_zap": record,
        "_time": now_epoch()
    }


# ---------- CONTEXTS ----------

def normalize_context(context):
    """
    Normalize a ZAP context record.
    """

    return {
        "event_type": "context",
        "context_name": context.get("context_name"),
        "context": context.get("context"),
        "source": "zaproxy",
        "_raw_zap": context,
        "_time": now_epoch()
    }


# ---------- DISPATCH ----------

def normalize(record_type, record):
    """
    Dispatch normalization by record type.
    """

    if record_type == "alert":
        return normalize_alert(record)

    if record_type == "site":
        return normalize_site(record)

    if record_type == "scan":
        return normalize_scan(record)

    if record_type == "context":
        return normalize_context(record)

    # Fallback: return raw
    return {
        "event_type": "unknown",
        "source": "zaproxy",
        "_raw_zap": record,
        "_time": now_epoch()
    }
