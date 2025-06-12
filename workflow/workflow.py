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
import sys

from scrapper.table_scrapper import *
from scrapper.project_details_scrapper import *
from exception.exceptions import SeleniumBotException
from custom_logging.my_logger import logger

class RERAScrapper:

    def __init__(self):
        self.url="https://rera.karnataka.gov.in/viewAllProjects"
        self.city="Vijayapura"
        self.driver=None

    def initiailise_browers(self):
        try:
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
            logger.info("Browser initialized successfully.")
        except Exception as e:
            logger.error(f"Error initializing browser: {e}")
            raise SeleniumBotException(e, sys)

    def get_url(self):
        try:
            self.initiailise_browers()
            self.driver.get(self.url)
            logger.info(f"Navigated to URL: {self.url}")
        except Exception as e:
            logger.error(f"Failed to navigate to URL: {e}")
            raise SeleniumBotException(e, sys)

    def city_selection(self):

        try:
            dropdown = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//select[@id='projectDist']"))
            )
            select = Select(dropdown)
            select.select_by_visible_text(self.city)
            logger.info(f"City '{self.city}' selected from dropdown.")

            search_button = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='btn1']"))
            )
            time.sleep(5)
            search_button.click()
            time.sleep(5)
        except TimeoutException as te:
            logger.error(f"City selection timed out: {te}")
            raise SeleniumBotException(te, sys)
        except Exception as e:
            logger.error(f"Error during city selection: {e}")
            raise SeleniumBotException(e, sys)

    def view_project_details_table_process(self):
        try:
            home_table_json = TableScrapper.home_table_json(self.driver)
            logger.info(f"Home table JSON extracted: {home_table_json}")

            project_details_button = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//a[@title='View Project Details']"))
            )
            project_details_button.click()
        except TimeoutException as te:
            logger.error(f"Project details table process timed out: {te}")
            raise SeleniumBotException(te, sys)
        except Exception as e:
            logger.error(f"Error during project details table process: {e}")
            raise SeleniumBotException(e, sys)
        
    def scrape_project_details(self):
        promoter_details=scrape_project_details.col_md("home", "Promoter", self.driver)
        authorized_signatory_details=scrape_project_details.col_md("home", "Authorized Signatory", self.driver)

        project_member_details=scrape_project_details.h1("home", "Project Member", self.driver)
        project_land_owner_details=scrape_project_details.h1("home", "Project Land Owner", self.driver)
        rera_registration_details_with_any_details=scrape_project_details.h1("home", "RERA Registration Details with any", self.driver)
        previous_project_details=scrape_project_details.h1("home", "Previous Project", self.driver)

        logger.info(f"Promoter Details 'promoter_details' scrapped.")
        logger.info(f"Authorized Signatory Detail 'authorized_signatory_details' scrapped.")
        logger.info(f"Project Member Details 'project_member_details' scrapped.")
        logger.info(f"Project Land Owner Details 'project_land_owner_details' scrapped.")
        logger.info(f"RERA Registration Details with any other State/UTs 'rera_registration_details_with_any_details' scrapped.")
        logger.info(f"Previous Project Details (Last 5 years only) 'previous_project_details' scrapped.")



        promoter_details=scrape_project_details.col_md("menu1", "Promoter", self.driver)
        
        # print(promoter_details)
        # print(authorized_signatory_details)
        # print(project_member_details)
        # print(project_land_owner_details)
        # print(rera_registration_details_with_any_details)
        # print(previous_project_details)

        time.sleep(60)








def main():
    scrapper = RERAScrapper()
    scrapper.get_url()
    scrapper.city_selection()
    scrapper.view_project_details_table_process()
    scrapper.scrape_project_details()


if __name__ == '__main__':
    main()