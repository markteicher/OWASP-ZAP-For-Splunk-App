# zap_input.py

import sys
import json

from splunklib.modularinput import Script, Event, Scheme, Argument

from zap_client import ZAPClient
from zap_collectors.alerts import collect_alerts


class ZAPInput(Script):

    def get_scheme(self):
        scheme = Scheme("ZAProxy Alerts Input")
        scheme.description = "Collect alerts from OWASP ZAP via API"
        scheme.use_external_validation = True
        scheme.streaming_mode_xml = False

        scheme.add_argument(
            Argument(
                name="zap_url",
                title="ZAP Base URL",
                description="Base URL of the ZAP instance (e.g. http://localhost:8080)",
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
        for input_name, input_item in inputs.inputs.items():

            zap_url = input_item["zap_url"]
            api_key = input_item["api_key"]
            verify_ssl = input_item.get("verify_ssl", "true").lower() == "true"

            zap = ZAPClient(
                base_url=zap_url,
                api_key=api_key,
                verify_ssl=verify_ssl
            )

            alerts = collect_alerts(zap)

            for alert in alerts:
                event = Event(
                    data=json.dumps(alert),
                    sourcetype="zap:alert"
                )
                ew.write_event(event)


if __name__ == "__main__":
    sys.exit(ZAPInput().run(sys.argv))
