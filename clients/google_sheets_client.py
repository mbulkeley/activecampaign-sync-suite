import logging
import backoff
from google.oauth2 import service_account
from googleapiclient.discovery import build


class GoogleSheetsClient:
    def __init__(self, service_account_file, spreadsheet_id):
        self.creds = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=['https://www.googleapis.com/auth/spreadsheets'])
        self.service = build('sheets', 'v4', credentials=self.creds, cache_discovery=False)
        self.spreadsheet_id = spreadsheet_id

    def _log_backoff(details):
        logging.warning(f"Backing off {details['wait']:0.1f} seconds after {details['tries']} tries "
                        f"calling function {details['target']} with args {details['args']} and kwargs {details['kwargs']}")

    def _log_giveup(details):
        logging.error(f"Giving up calling function {details['target']} after {details['tries']} tries")
