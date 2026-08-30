"""
ActiveCampaign Information to Google Sheet for record keeping.

Data Integration Tool: Google Sheets, Google Docs, Slack, and ActiveCampaign

Author: Michael B.
Version: 1.0.0

Description:
    This program provides functionalities to interact with Google Sheets, Google Docs,
    ActiveCampaign, and Slack.
    - GoogleSheetsClient: A class to handle interactions with Google Sheets API.
    - GoogleDocsClient: A class to handle interactions with Google Docs API.
    - ActiveCampaignClient: A class to manage communications with ActiveCampaign API.
    - SlackClient: A class to manage communications with Slack API.
    - Main functionality: Orchestrates the process of data fetching from ActiveCampaign,
      processing this data, and updating it in Google Sheets & Docs and sending any notifications
      to Slack.

Changelog:
    1.0.0 (2024-08-08): Initial release to pull automation information from ActiveCampaign and push
                        this information to Google.

License:
    Apache-2.0 license
"""

__version__ = "1.0.0"

import warnings

warnings.filterwarnings('ignore')
import os
import logging
from datetime import datetime
from clients.active_campaign_client import ActiveCampaignClient
from clients.google_sheets_client import GoogleSheetsClient
from clients.google_docs_client import GoogleDocsClient
from clients.slack_client import SlackClient

# Configure logging
os.makedirs('logs', exist_ok=True)
log_file_path = os.path.join('logs', 'activecampaign_to_google.log')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]
)

logging.info('*** STARTING ***')
now = datetime.now()
date_time_str = now.strftime("%d-%m-%Y %H:%M")
logging.debug(f"'Last updated', {date_time_str}")


def main():
    ac_apikey = os.environ.get('ACTIVECAMPAIGN_API_KEY')
    ac_base_url = os.environ.get('ACTIVECAMPAIGN_BASE_URL')
    google_key_path = os.environ.get('GOOGLE_KEY_PATH', 'config/google_api_key.json')
    google_spreadsheet_id = os.environ.get('ACTIVECAMPAIGN_SPREADSHEET_ID')

    logging.debug(f"ActiveCampaign API Key: {ac_apikey}")
    logging.debug(f"ActiveCampaign Base URL: {ac_base_url}")
    logging.debug(f"Google Key Path: {google_key_path}")
    logging.debug(f"Google Spreadsheet ID: {google_spreadsheet_id}")

    ac_client = ActiveCampaignClient(ac_apikey, ac_base_url)
    gs_client = GoogleSheetsClient(google_key_path, google_spreadsheet_id)

    results = ac_client.get_automations()
    logging.debug(results)
    logging.info("*** DONE ***")


if __name__ == '__main__':
    main()
