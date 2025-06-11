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

    





if __name__ == '__main__':
    scrapper = RERAScrapper()
    scrapper.get_url()
    scrapper.city_selection()