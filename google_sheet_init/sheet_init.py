import gspread
from google.oauth2.service_account import Credentials
import sys
from exception.exceptions import SeleniumBotException
import os

# Add the project root to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from custom_logging.my_logger import logger

from config.config_loader import load_config

config=load_config()

class Google_sheet_init:

    def __init__(self):
        self.google_credentials=config["sheet_info"]["credential_json"]
        self.sheet_url=config["sheet_info"]["sheet_link"]
        self.sub_sheet=config["sheet_info"]["subsheet_name"]

    def sheet(self):
        # Google Sheets configuration
        gc = gspread.service_account(filename=self.google_credentials)  # Replace with the path to your credentials.json file

        # Open the Google Sheet by URL
        sh = gc.open_by_url(self.sheet_url)

        try:
            worksheet = sh.worksheet(self.sub_sheet)
            # print(f"Worksheet '{self.sub_sheet}' found.")
            logger.info(f"Worksheet '{self.sub_sheet}' found.")
        except gspread.exceptions.WorksheetNotFound:
            worksheet = sh.add_worksheet(title=self.sub_sheet, rows="1000", cols="100")
            # print(f"Worksheet '{self.sub_sheet}' created.")
            logger.error(f"Worksheet '{self.sub_sheet}' created.")

        return worksheet
    
if __name__ == '__main__':
    try:
        google_sheet = Google_sheet_init()
        google_sheet.sheet()
    except Exception as e:
        print(f"\n🔴▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬🔴\n")
        logger.error(f"An error occurred: {str(e)}")  # Log the error first
        raise SeleniumBotException(e, sys)  # Raise the custom exception
