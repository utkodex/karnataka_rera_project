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
from utils.utita_tools import SimpleTools

class RERAScrapper:

    def __init__(self):
        self.url="https://rera.karnataka.gov.in/viewAllProjects"
        self.city="Kolar"
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
            time.sleep(1)
            search_button.click()
            logger.info(f"Select Button Clicked.")
            time.sleep(1)
        except TimeoutException as te:
            logger.error(f"City selection timed out: {te}")
            raise SeleniumBotException(te, sys)
        except Exception as e:
            logger.error(f"Error during city selection: {e}")
            raise SeleniumBotException(e, sys)

    def view_project_details_table_process(self, i):
        try:
            home_table_json = TableScrapper.home_table_json(self.driver)
            logger.info(f"Home table JSON extracted: home_table_json")

            # project_details_button = WebDriverWait(self.driver, 20).until(
            #     EC.presence_of_element_located((By.XPATH, "//a[@title='View Project Details']"))
            # )
            project_details_button = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"//tbody/tr[{i}]/td[4]"))
            )
            project_details_button.click()
        except TimeoutException as te:
            logger.error(f"Project details table process timed out: {te}")
            raise SeleniumBotException(te, sys)
        except Exception as e:
            logger.error(f"Error during project details table process: {e}")
            raise SeleniumBotException(e, sys)
        
    def scrape_project_details(self):
        try:
            promoter_details=scrape_project_details.col_md("home", "Promoter", self.driver)
            authorized_signatory_details=scrape_project_details.col_md("home", "Authorized Signatory", self.driver)

            project_member_details=scrape_project_details.h1("home", "Project Member", "Details", self.driver)
            project_land_owner_details=scrape_project_details.h1("home", "Project Land Owner", "Details", self.driver)
            rera_registration_details_with_any_details=scrape_project_details.h1("home", "RERA Registration Details with any", "Details", self.driver)
            previous_project_details=scrape_project_details.h1("home", "Previous Project", "Details", self.driver)

            logger.info(f"Promoter Details 'promoter_details' scrapped.")
            logger.info(f"Authorized Signatory Detail 'authorized_signatory_details' scrapped.")
            logger.info(f"Project Member Details 'project_member_details' scrapped.")
            logger.info(f"Project Land Owner Details 'project_land_owner_details' scrapped.")
            logger.info(f"RERA Registration Details with any other State/UTs 'rera_registration_details_with_any_details' scrapped.")
            logger.info(f"Previous Project Details (Last 5 years only) 'previous_project_details' scrapped.")

            time.sleep(2)

            # =============================================== Project Details =============================================== #

            try:
                project_details_page = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH,"//a[normalize-space()='Project Details']")))
                project_details_page.click()
                logger.info(f"Project Details page clicked.")
            except TimeoutException as te:
                logger.error(f"Timed out waiting for Project Details page: {te}")
                # raise SeleniumBotException(te, sys)

            if project_details_page:
                project_details=scrape_project_details.col_md("menu1", "Project", self.driver, "Project Details")
                development_details=scrape_project_details.h1("menu1", "Development", "Details", self.driver)
                external_development_work=scrape_project_details.h1("menu1", "External Development", "Work", self.driver)
                other_external_development_work=scrape_project_details.h1("menu1", "Other External Development", "Work", self.driver)
                project_bank_details=scrape_project_details.h1("menu1", "Project Bank ( Escrow Account )", "Details", self.driver)
                project_agents=scrape_project_details.h1("menu1", "Project", "Agents", self.driver)

                project_detail_table=TableScrapper.project_detial_table_json_creator(self.driver)

                logger.info(f"Project Details 'project_details' scrapped.")
                logger.info(f"Development Details 'development_details' scrapped.")
                logger.info(f"External Development Work 'external_development_work' scrapped.")
                logger.info(f"Other External Development Work 'other_external_development_work' scrapped.")
                logger.info(f"Project Bank ( Escrow Account ) Details 'project_bank_details' scrapped.")
                logger.info(f"Project Agents 'project_agents' scrapped.")
                logger.info(f"Project Detail Table 'project_detail_table' scrapped.")

            # =============================================== Uploaded Documents =============================================== #

            try:
                uploaded_documents_page = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH,"//a[normalize-space()='Uploaded Documents']")))
                uploaded_documents_page.click()
                logger.info(f"Uploaded Documents page clicked.")
            except TimeoutException as te:
                logger.error(f"Timed out waiting for Uploaded Documents page: {te}")
                # raise SeleniumBotException(te, sys)

            if uploaded_documents_page:    
                project_documents=scrape_project_details.uploaded_doc_extractor("Project", "Documents", self.driver)
                project_approval=scrape_project_details.uploaded_doc_extractor("Project", "Approval", self.driver)
                declaration=scrape_project_details.uploaded_doc_extractor("Declaration", "", self.driver)
                other_documents=scrape_project_details.uploaded_doc_extractor("Other Documents", "", self.driver)
                project_photo=scrape_project_details.uploaded_doc_extractor("Project", "Photo", self.driver)
                
                financial_document=TableScrapper.financial_document_json_creator(self.driver)

                logger.info(f"Project Documents 'project_documents' scrapped.")
                logger.info(f"Project Approval 'project_approval' scrapped.")
                logger.info(f"Declaration 'declaration' scrapped.")
                logger.info(f"Other Documents 'other_documents' scrapped.")
                logger.info(f"Project Photo 'project_photo' scrapped.")
                logger.info(f"Financial Document 'financial_document' scrapped.")

            # =============================================== Completion Details =============================================== #

            try:
                completion_details_page = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='Completion Details']"))
                )
                completion_details_page.click()
                logger.info(f"Completion Details page clicked.")
            except TimeoutException as te:
                logger.error(f"Timed out waiting for Completion Details page: {te}")
                # raise SeleniumBotException(te, sys)
            
            if completion_details_page:
                completion_details=scrape_project_details.completion_details("Completion", "Details", self.driver)

                logger.info(f"Completion Details '{completion_details}' scrapped.")

        except TimeoutException as te:
            logger.error(f"Timeout occurred in scrape_project_details: {te}")
            # raise SeleniumBotException(te, sys)
        except NoSuchElementException as ne:
            logger.error(f"Element not found in scrape_project_details: {ne}")
            # raise SeleniumBotException(ne, sys)
        except Exception as e:
            logger.error(f"An error occurred in scrape_project_details: {e}")
            # raise SeleniumBotException(e, sys)
        
    def table_iter(self, page_num):

        project_details_button = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, f"//tbody/tr/td[4]"))
            )
        num_of_iter=len(project_details_button)+1

        for i in range(1, num_of_iter):

            self.view_project_details_table_process(i)

            self.scrape_project_details()
            
            time.sleep(2)

            try:
                checking_project_details = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, "//body/section[@id='site-content']/div[@class='pop_main']/div[@id='project_details_popup']/div[@class='modal-dialog-lg']/div[@class='modal-content']/div[@class='modal-body']/div[@id='result']/section[@id='site-content']/div[1]"))
                )
            except TimeoutException:
                print(f"Row {i} not clickable. Skipping.")
                # continue
                checking_project_details=None

            if checking_project_details:
                print("Project Details Pages")
                self.driver.back()

                try:
                    project_details_button = WebDriverWait(self.driver, 2).until(
                            EC.element_to_be_clickable((By.XPATH, f"//tbody/tr[{i}]/td[4]"))
                        )
                except TimeoutException:
                    print(f"table disappeared")
                    # continue
                    project_details_button = None
                
                if not project_details_button:

                    self.city_selection()
                    
                    time.sleep(2)

                # page_num=1
                SimpleTools.page_number_finder(page_num, self.driver)

                time.sleep(4)

            print("-"*150)

    def page_iter(self):

        largest_num = SimpleTools.largest_page_number(self.driver)
        for i in range (largest_num):
            page_num=i+1

            pages = SimpleTools.ava_page_number(self.driver)
            second_largest=SimpleTools.second_largest_number(pages)
            print(f"{page_num} : {second_largest}")

            while page_num > second_largest:
                print(second_largest)
                try:
                    next_page_button = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, f"//a[@class='paginate_button '][normalize-space(text())='{second_largest}']")))
                    next_page_button.click()
                    second_largest += 1
                    time.sleep(2)
                except TimeoutException:
                    print("No more pages available.")
                    break

            # print(page_num)
            if page_num > 1:

                print("Page Num: ", page_num)
                next_button_element = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, f"//a[@class='paginate_button '][normalize-space(text())='{page_num}']"))
                )
                next_button_element.click()
                
                time.sleep(2)

            self.table_iter(page_num)

                


        








def main():
    scrapper = RERAScrapper()
    scrapper.initiailise_browers()
    scrapper.get_url()
    scrapper.city_selection()
    # scrapper.view_project_details_table_process()
    # scrapper.scrape_project_details()
    scrapper.page_iter()
    time.sleep(20000)


if __name__ == '__main__':
    main()