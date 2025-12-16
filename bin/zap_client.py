# zap_client.py

import requests


class ZAPClient:
    def __init__(self, base_url, api_key, timeout=30, verify_ssl=True):
        """
        Initialize ZAP API client.

        :param base_url: ZAP base URL (e.g. http://localhost:8080)
        :param api_key: ZAP API key
        :param timeout: HTTP timeout in seconds
        :param verify_ssl: verify TLS certs if using HTTPS
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.verify_ssl = verify_ssl

    def get(self, path, params=None):
        """
        Perform a GET request against the ZAP API.

        :param path: API path (e.g. /JSON/core/view/alerts/)
        :param params: dict of query parameters
        :return: parsed JSON response
        """
        if params is None:
            params = {}

        # ZAP expects API key as query param
        params["apikey"] = self.api_key

        url = f"{self.base_url}{path}"

        response = requests.get(
            url,
            params=params,
            timeout=self.timeout,
            verify=self.verify_ssl
        )

        response.raise_for_status()

        return response.json()
