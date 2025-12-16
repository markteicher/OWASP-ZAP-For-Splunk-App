# zap_input.py

import sys
import json

from splunklib.modularinput import Script, Event, Scheme, Argument

from zap_client import ZAPClient
from zap_collectors.alerts import collect_alerts
from zap_collectors.sites import collect_sites
from zap_collectors.scans import collect_scans
from zap_collectors.contexts import collect_contexts


class ZAPInput(Script):

    def get_scheme(self):
        scheme = Scheme("ZAProxy Modular Input")
        scheme.description = "Collect data from OWASP ZAP via API"
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
                description="API key for ZAP",
                required_on_create=True,
                data_type=Argument.data_type_string
            )
        )

        scheme.add_argument(
            Argument(
                name="verify_ssl",
                title="Verify SSL",
                description="Verify SSL certificates",
                required_on_create=False
            )
        )

        return scheme

    def stream_events(self, inputs, ew):
        for stanza, item in inputs.inputs.items():

            zap_url = item["zap_url"]
            api_key = item["api_key"]
            verify_ssl = item.get("verify_ssl", "true").lower() == "true"

            zap = ZAPClient(
                base_url=zap_url,
                api_key=api_key,
                verify_ssl=verify_ssl
            )

            # Determine feed type from stanza
            if stanza.startswith("zaproxy_alerts://"):
                records = collect_alerts(zap)
                sourcetype = "zap:alert"

            elif stanza.startswith("zaproxy_sites://"):
                records = collect_sites(zap)
                sourcetype = "zap:site"

            elif stanza.startswith("zaproxy_scans://"):
                records = collect_scans(zap)
                sourcetype = "zap:scan"

            elif stanza.startswith("zaproxy_contexts://"):
                records = collect_contexts(zap)
                sourcetype = "zap:context"

            else:
                # Unknown stanza type – skip safely
                continue

            for record in records:
                event = Event(
                    data=json.dumps(record),
                    sourcetype=sourcetype
                )
                ew.write_event(event)


if __name__ == "__main__":
    sys.exit(ZAPInput().run(sys.argv))
