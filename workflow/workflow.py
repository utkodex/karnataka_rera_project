from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
import os
import time
import pandas as pd
from pandas import DataFrame
from datetime import datetime
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import pickle
import gspread
from google.oauth2.service_account import Credentials
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import json
from google_sheet_init.sheet_init import Google_sheet_init

class RERAScrapper:

    def __init__(self):
        self.url="https://rera.karnataka.gov.in/viewAllProjects"
        self.city="Vijayapura"

    def initiailise_browers(self):
        # Create a fake user-agent
        ua = UserAgent()
        fake_user_agent = ua.random  # Get a random user-agent

        # Set up undetected-chromedriver
        options = uc.ChromeOptions()
        options.add_argument(f"user-agent={fake_user_agent}") 
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-cache")
        options.add_argument("--aggressive-cache-discard")
        options.add_argument("--disable-application-cache")
        options.add_argument("--disable-offline-load-stale-cache")
        options.add_argument("--disk-cache-size=0")
        # Uncomment if you want headless mode
        # options.add_argument("--headless=new")

        # Initialize undetected-chromedriver
        self.driver = uc.Chrome(version_main=137, options=options)

    def get_url(self):
        self.initiailise_browers()
        self.driver.get(self.url)

    def city_selection(self):

        # Wait for the dropdown element to be present
        dropdown = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//select[@id='projectDist']"))
        )

        # Use the Select class to interact with the dropdown
        select = Select(dropdown)

        # Select the option by its visible text
        select.select_by_visible_text(self.city)

        # Optionally, print the selected option to verify
        selected_option = select.first_selected_option.text
        print(f"Selected option: {selected_option}")

        search_button_element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH,"//input[@name='btn1']")))
        search_button_element.click()
        time.sleep(10)

    def extractor(self):

        # Wait for the project_details element
        project_contains = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='menu1']//form[@class='form-horizontal']"))
        )

        # Get the HTML content of the element
        project_html = project_contains.get_attribute("outerHTML")

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(project_html, "html.parser")

        # Find all rows in the structure
        rows = soup.find_all("div", class_="row", style="font-size: 13px;")

        # Initialize dictionary to store JSON data
        project_data = {}

        # Extract and populate data
        for row in rows:
            headings = row.find_all("div", class_="col-md-3 col-sm-6 col-xs-6")
            for i in range(0, len(headings), 2):  # Step by 2 to pair heading and content
                heading = headings[i].get_text(strip=True).replace(":", "")
                content = headings[i + 1].get_text(strip=True) if i + 1 < len(headings) else ""
                project_data[heading] = content

        # Convert dictionary to JSON
        project_json = json.dumps(project_data, indent=4)

        # Print the JSON formatted output
        print("project_json")
        return project_json

    def view_project_iterator(self):

        for _ in range(5):
            body_element = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, "//body"))
                    )
            body_element.send_keys(Keys.PAGE_DOWN)
        
        project_details = WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,"//a[@title='View Project Details']")))
        project_details=len(project_details)
        print(project_details)

        for s_no in range(project_details):

            print("S.no. ", s_no+1)
            project_details = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH,f"(//a[@title='View Project Details'])[{s_no+1}]")))
            project_details.click()
            time.sleep(2)

            project_details_button = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH,"//a[normalize-space()='Project Details']")))
            project_details_button.click()
            time.sleep(2)

            project_json=self.extractor()

            self.driver.back()
            time.sleep(5)

            self.city_selection()

            google_sheet = Google_sheet_init()  # Create an instance of Google_sheet_init
            worksheet = google_sheet.sheet()  # Call the sheet method on the instance

            data_list = []

            # Replace None or empty values in the dictionary with "N/A"
            data_dict = {key: (value if value else "N/A") for key, value in {
                'JSON data' : project_json,
                'City': self.city,
            }.items()}

            # Append the dictionary to the list
            data_list.append(data_dict)

            # Append data to the Google Sheet
            worksheet.append_rows([list(data_dict.values())], value_input_option="RAW")

    def page_iter(self):
        while True:

            self.view_project_iterator()

            try:
                # Check if the "disabled" next button is present
                disabled_next_button = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, "//a[@class='paginate_button next disabled']"))
                )
            except:
                # If the "disabled" next button is not found, set it to None
                disabled_next_button = None

            # Print the status of the disabled button for debugging
            print(f"Disabled button detected: {disabled_next_button}")

            if disabled_next_button:
                # If the disabled next button is detected, stop the loop
                print("No more pages to navigate.")
                break

            try:
                # Locate and click the next button
                next_button_element = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//a[@id='approvedTable_next']"))
                )
                next_button_element.click()
                print("Navigated to the next page.")
                time.sleep(2)
            except Exception as e:
                # Handle exceptions if the next button is not clickable
                print(f"Error while clicking next button: {e}")
                break





if __name__ == '__main__':
    scrapper = RERAScrapper()
    scrapper.get_url()
    scrapper.city_selection()
    scrapper.page_iter()