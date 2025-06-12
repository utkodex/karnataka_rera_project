import gspread
from google.oauth2.service_account import Credentials
import sys
from exception.exceptions import SeleniumBotException
import os

# Add the project root to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from custom_logging.my_logger import logger

class Google_sheet_init:

    def __init__(self):
        self.google_credentials="credentials.json"
        self.sheet_url="https://docs.google.com/spreadsheets/d/1lnVDiO3xTA43cIDGd5OEoxC2P1hFFpM9L5BQw2AIxUs/edit?gid=0#gid=0"
        self.sub_sheet="RERA JSON Data"

    def sheet(self):
        # Google Sheets configuration
        gc = gspread.service_account(filename=self.google_credentials)  # Replace with the path to your credentials.json file

        # Open the Google Sheet by URL
        sh = gc.open_by_url(self.sheet_url)

        try:
            # Try to open the subsheet by title
            worksheet = sh.worksheet(self.sub_sheet)
            print(f"Worksheet '{self.sub_sheet}' found.")
        except gspread.exceptions.WorksheetNotFound:
            # If subsheet is not found, create it
            worksheet = sh.add_worksheet(title=self.sub_sheet, rows="1000", cols="100")
            print(f"Worksheet '{self.sub_sheet}' created.")

        return worksheet
    
if __name__ == '__main__':
    try:
        google_sheet = Google_sheet_init()
        google_sheet.sheet()
    except Exception as e:
        print(f"\n🔴▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬🔴\n")
        logger.error(f"An error occurred: {str(e)}")  # Log the error first
        raise SeleniumBotException(e, sys)  # Raise the custom exception
