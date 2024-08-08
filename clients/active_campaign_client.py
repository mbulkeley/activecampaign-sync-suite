import requests
import logging
import backoff

class ActiveCampaignClient:
    def __init__(self, api_key, base_url):
        self.session = requests.Session()
        self.api_key = api_key
        self.headers = {"Accept": "application/json", "Api-Token": api_key}
        self.base_url = base_url

    def _log_backoff(details):
        logging.warning(f"Backing off {details['wait']:0.1f} seconds after {details['tries']} tries "
                        f"calling function {details['target']} with args {details['args']} and kwargs {details['kwargs']}")

    def _log_giveup(details):
        logging.error(f"Giving up calling function {details['target']} after {details['tries']} tries")

    @backoff.on_exception(
        backoff.expo,
        requests.exceptions.RequestException,
        max_tries=5,
        on_backoff=_log_backoff,
        on_giveup=_log_giveup)
    def get_automations(self):
        url = f"{self.base_url}/api/3/automations"
        response = self.session.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
