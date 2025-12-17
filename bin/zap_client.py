# zap_client.py

import requests
import time

from zap_utils import (
    get_logger,
    retry_loop,
    duration_seconds,
    format_exception,
)


class ZAPClient:
    """
    Production ZAP API client for Splunk.
    """

    def __init__(
        self,
        base_url,
        api_key,
        timeout=30,
        verify_ssl=True,
        retries=3,
        retry_delay=2.0
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.retries = retries
        self.retry_delay = retry_delay

        self.logger = get_logger("zaproxy.client")

        self.session = requests.Session()
        self.session.verify = verify_ssl
        self.session.headers.update({
            "User-Agent": "ZAProxy-Splunk-App/1.0"
        })

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get(self, path, params=None):
        """
        Perform a GET request against the ZAP API with retries.
        """
        return retry_loop(
            attempts=self.retries,
            delay=self.retry_delay,
            logger=self.logger,
            fn=self._get_once,
            path=path,
            params=params
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_once(self, path, params=None):
        if params is None:
            params = {}

        params["apikey"] = self.api_key

        url = f"{self.base_url}{path}"

        start = time.time()

        try:
            response = self.session.get(
                url,
                params=params,
                timeout=self.timeout
            )

            elapsed = duration_seconds(start)

            self.logger.debug(
                "GET %s status=%s duration=%ss",
                url,
                response.status_code,
                elapsed
            )

            response.raise_for_status()

            return response.json()

        except Exception as exc:
            elapsed = duration_seconds(start)

            self.logger.error(
                "ZAP API GET failed url=%s duration=%ss error=%s",
                url,
                elapsed,
                exc
            )

            raise exc
