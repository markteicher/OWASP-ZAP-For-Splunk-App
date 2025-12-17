# zap_input.py

import sys

from splunklib.modularinput import Script, Event, Scheme, Argument

from zap_client import ZAPClient
from zap_collectors.alerts import collect_alerts
from zap_collectors.sites import collect_sites
from zap_collectors.scans import collect_scans
from zap_collectors.contexts import collect_contexts
from zap_normalize import normalize
from zap_utils import (
    get_logger,
    bool_from_string,
    safe_json_dumps,
    format_exception,
)


class ZAPInput(Script):

    def get_scheme(self):
        scheme = Scheme("ZAProxy Modular Input")
        scheme.description = "Collect OWASP ZAP data via API"
        scheme.use_external_validation = True
        scheme.streaming_mode_xml = False

        scheme.add_argument(
            Argument(
                name="zap_url",
                title="ZAP Base URL",
                description="Base URL of the ZAP instance",
                required_on_create=True
            )
        )

        scheme.add_argument(
            Argument(
                name="api_key",
                title="ZAP API Key",
                description="ZAP API key",
                required_on_create=True
            )
        )

        scheme.add_argument(
            Argument(
                name="verify_ssl",
                title="Verify SSL",
                description="Verify TLS certificates",
                required_on_create=False
            )
        )

        return scheme

    # ------------------------------------------------------------------

    def stream_events(self, inputs, ew):
        logger = get_logger("zaproxy.input")

        for stanza, item in inputs.inputs.items():

            zap_url = item["zap_url"]
            api_key = item["api_key"]
            verify_ssl = bool_from_string(item.get("verify_ssl"), default=True)

            zap = ZAPClient(
                base_url=zap_url,
                api_key=api_key,
                verify_ssl=verify_ssl
            )

            try:
                if stanza.startswith("zaproxy_alerts://"):
                    records = collect_alerts(zap)
                    record_type = "alert"
                    sourcetype = "zap:alert"

                elif stanza.startswith("zaproxy_sites://"):
                    records = collect_sites(zap)
                    record_type = "site"
                    sourcetype = "zap:site"

                elif stanza.startswith("zaproxy_scans://"):
                    records = collect_scans(zap)
                    record_type = "scan"
                    sourcetype = "zap:scan"

                elif stanza.startswith("zaproxy_contexts://"):
                    records = collect_contexts(zap)
                    record_type = "context"
                    sourcetype = "zap:context"

                else:
                    logger.warning("Unknown input stanza: %s", stanza)
                    continue

                for record in records:
                    normalized = normalize(record_type, record)

                    event = Event(
                        data=safe_json_dumps(normalized),
                        sourcetype=sourcetype
                    )
                    ew.write_event(event)

            except Exception as exc:
                error_event = {
                    "event_type": "error",
                    "stanza": stanza,
                    "zap_url": zap_url,
                    "error": format_exception(exc),
                    "source": "zaproxy"
                }

                ew.write_event(
                    Event(
                        data=safe_json_dumps(error_event),
                        sourcetype="zap:error"
                    )
                )

                logger.error(
                    "Failed processing stanza %s: %s",
                    stanza,
                    exc
                )


if __name__ == "__main__":
    sys.exit(ZAPInput().run(sys.argv))
