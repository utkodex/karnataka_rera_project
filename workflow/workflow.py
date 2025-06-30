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
from config.config_loader import load_config

class RERAScrapper:

    def __init__(self, city, headless=True):
        self.url="https://rera.karnataka.gov.in/viewAllProjects"
        self.city=city
        self.driver=None
        self.headless = headless

    def initiailise_browers(self):
        try:
            ua = UserAgent()
            fake_user_agent = ua.random 

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

            if self.headless:
                options.add_argument("--headless=new")

            config=load_config()
            self.driver = uc.Chrome(version_main=config["chrome-driver-version"], options=options)
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
            home_table_json = TableScrapper.home_table_json(self.driver, i)
            logger.info(f"Home table JSON extracted: home_table_json")

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
        
        return home_table_json
        
    def scrape_project_details(self, home_table_json):
        try:

            # Initialize variables to avoid UnboundLocalError
            project_details_page = None
            uploaded_documents_page = None
            completion_details_page = None

            complaint_page = None
            complaint_on_project_page = None

            completion_details_page = None
            
            # print(f"home_table_json", "home_table_json")
            logger.info(f"Home Table JSON 'home_table_json' scrapped.")

            # ===========================================================================================================================================================================

            promoter_details=None
            authorized_signatory_details=None
            project_member_details=None
            project_land_owner_details=None
            rera_registration_details_with_any_details=None
            previous_project_details=None
            # -----------------------------------
            project_details=None
            development_details=None
            project_ongoing_status=None
            external_development_work=None
            other_external_development_work=None
            project_bank_details=None
            project_agents=None
            project_detail_table=None
            # -----------------------------------
            project_documents=None
            project_approval=None
            declaration=None
            other_documents=None
            project_photo=None
            financial_document=None
            # -----------------------------------
            promoter_table=None
            project_table=None
            # -----------------------------------
            completion_details=None
            development_details_completion=None
            uploaded_documents=None
            photos_uploaded=None

            # ===========================================================================================================================================================================

            time.sleep(2)
            
            try:
                promoter_details=scrape_project_details.col_md("home", "Promoter", self.driver)
                logger.info(f"Promoter Details 'promoter_details' scrapped.")
            except Exception as e:
                logger.warning(f"Promoter Details 'promoter_details' **************not************** scrapped.")

            try:
                authorized_signatory_details=scrape_project_details.col_md("home", "Authorized Signatory", self.driver)
                logger.info(f"Authorized Signatory Detail 'authorized_signatory_details' scrapped.")
            except Exception as e:
                logger.warning(f"Authorized Signatory Detail 'authorized_signatory_details' **************not************** scrapped.")

            try:
                project_member_details=scrape_project_details.h1("home", "Project Member", "Details", self.driver)
                logger.info(f"Project Member Details 'project_member_details' scrapped.")
            except Exception as e:
                logger.warning(f"Project Member Details 'project_member_details' **************not************** scrapped.")

            try:
                project_land_owner_details=scrape_project_details.h1("home", "Project Land Owner", "Details", self.driver)
                logger.info(f"Project Land Owner Details 'project_land_owner_details' scrapped.")
            except Exception as e:
                logger.warning(f"Project Land Owner Details 'project_land_owner_details' **************not************** scrapped.")

            try:
                rera_registration_details_with_any_details=scrape_project_details.h1("home", "RERA Registration Details with any", "Details", self.driver)
                logger.info(f"RERA Registration Details with any other State/UTs 'rera_registration_details_with_any_details' scrapped.")
            except Exception as e:
                logger.warning(f"RERA Registration Details with any other State/UTs 'rera_registration_details_with_any_details' **************not************** scrapped.")

            try:
                previous_project_details=scrape_project_details.h1("home", "Previous Project", "Details", self.driver)
                logger.info(f"Previous Project Details (Last 5 years only) 'previous_project_details' scrapped.")
            except Exception as e:
                logger.warning(f"Previous Project Details (Last 5 years only) 'previous_project_details' **************not************** scrapped.")

            # =============================================== Project Details =============================================== #

            try:
                project_details_page = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH,"//a[normalize-space()='Project Details']")))
                project_details_page.click()
                logger.info(f"Project Details page clicked.")
            except TimeoutException as te:
                logger.error(f"Timed out waiting for Project Details page: {te}")

            time.sleep(2)

            if project_details_page:
                try:
                    project_details=scrape_project_details.col_md("menu1", "Project", self.driver, "Project Details")
                    logger.info(f"Project Details 'project_details' scrapped.")
                except Exception as e:
                    logger.warning(f"Project Details 'project_details' **not** scrapped.")

                try:
                    development_details=scrape_project_details.h1("menu1", "Development", "Details", self.driver)
                    logger.info(f"Development Details 'development_details' scrapped.")
                except Exception as e:
                    logger.warning(f"Development Details 'development_details' **not** scrapped.")
                
                try:
                    project_ongoing_status=scrape_project_details.h1("menu1", "Project Ongoing", "Status", self.driver)
                    logger.info(f"Project Ongoing Status 'project_ongoing_status' scrapped.")
                except Exception as e:
                    logger.warning(f"Project Ongoing Status 'project_ongoing_status' **not** scrapped.")
                
                try:
                    external_development_work=scrape_project_details.h1("menu1", "External Development", "Work", self.driver)
                    logger.info(f"External Development Work 'external_development_work' scrapped.")
                except Exception as e:
                    logger.warning(f"External Development Work 'external_development_work' **not** scrapped.")

                try:
                    other_external_development_work=scrape_project_details.h1("menu1", "Other External Development", "Work", self.driver)
                    logger.info(f"Other External Development Work 'other_external_development_work' scrapped.")
                except Exception as e:
                    logger.warning(f"Other External Development Work 'other_external_development_work' **not** scrapped.")

                try:
                    project_bank_details=scrape_project_details.h1("menu1", "Project Bank ( Escrow Account )", "Details", self.driver)
                    logger.info(f"Project Bank ( Escrow Account ) Details 'project_bank_details' scrapped.")
                except Exception as e:
                    logger.warning(f"Project Bank ( Escrow Account ) Details 'project_bank_details' **not** scrapped.")

                try:
                    project_agents=scrape_project_details.h1("menu1", "Project", "Agents", self.driver)
                    logger.info(f"Project Agents 'project_agents' scrapped.")
                except Exception as e:
                    logger.warning(f"Project Agents 'project_agents' **not** scrapped.")


                try:
                    project_detail_table=TableScrapper.project_detial_table_json_creator(self.driver)
                    logger.info(f"Project Detail Table 'project_detail_table' scrapped.")
                except Exception as e:
                    logger.warning(f"Project Detail Table 'project_detail_table' **not** scrapped.")

            # =============================================== Uploaded Documents =============================================== #

            try:
                uploaded_documents_page = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH,"//a[normalize-space()='Uploaded Documents']")))
                uploaded_documents_page.click()
                logger.info(f"Uploaded Documents page clicked.")
            except TimeoutException as te:
                logger.error(f"Timed out waiting for Uploaded Documents page: {te}")

            time.sleep(2)

            if uploaded_documents_page:  
                try:  
                    project_documents=scrape_project_details.uploaded_doc_extractor("Project", "Documents", self.driver)
                    logger.info(f"Project Documents 'project_documents' scrapped.")
                except Exception as e:
                    logger.warning(f"Project Documents 'project_documents' **not** scrapped.")

                try:  
                    project_approval=scrape_project_details.uploaded_doc_extractor("Project", "Approval", self.driver)
                    logger.info(f"Project Approval 'project_approval' scrapped.")
                except Exception as e:
                    logger.warning(f"Project Approval 'project_approval' **not** scrapped.")

                try:  
                    declaration=scrape_project_details.uploaded_doc_extractor("Declaration", "", self.driver)
                    logger.info(f"Declaration 'declaration' scrapped.")
                except Exception as e:
                    logger.warning(f"Declaration 'declaration' **not** scrapped.")

                try:  
                    other_documents=scrape_project_details.uploaded_doc_extractor("Other Documents", "", self.driver)
                    logger.info(f"Other Documents 'other_documents' scrapped.")
                except Exception as e:
                    logger.warning(f"Other Documents 'other_documents' **not** scrapped.")

                try:  
                    project_photo=scrape_project_details.uploaded_doc_extractor("Project", "Photo", self.driver)
                    logger.info(f"Project Photo 'project_photo' scrapped.")
                except Exception as e:
                    logger.warning(f"Project Photo 'project_photo' **not** scrapped.")

                try:  
                    financial_document=TableScrapper.financial_document_json_creator(self.driver)
                    logger.info(f"Financial Document 'financial_document' scrapped.")
                except Exception as e:
                    logger.warning(f"Financial Document 'financial_document' **not** scrapped.")

            # =============================================== Complaint Details =============================================== #

            try:
                complaint_page = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH,"//a[normalize-space()='Complaints']")))
                complaint_page.click()
                logger.info(f"Complaint page clicked.")
            except TimeoutException as te:
                logger.error(f"Timed out waiting for Complaint page: {te}")

            time.sleep(2)

            if complaint_page:
                try:  
                    promoter_table=TableScrapper.complaints_scrapper("Complaints On this Promoter", self.driver)
                    logger.info(f"Promoter Table 'promoter_table' scrapped.")
                except Exception as e:
                    logger.warning(f"Promoter Table 'project_table' **not** scrapped.")

                time.sleep(2)
                try: 
                    complaint_on_project_page = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH,"//a[contains(normalize-space(), 'Complaints On this Project')]")))
                    complaint_on_project_page.click()
                    logger.info(f"Project Complaint sub-page clicked.")
                except TimeoutException as te:
                    logger.error(f"Timed out waiting for Project Complaint sub-page: {te}")

                if complaint_on_project_page:
                    try:  
                        project_table=TableScrapper.complaints_scrapper("Complaints On this Project", self.driver)
                        logger.info(f"Other Documents 'project_table' scrapped.")
                    except Exception as e:
                        logger.warning(f"Other Documents 'project_table' **not** scrapped.")

            # =============================================== Completion Details =============================================== #

            try:
                completion_details_page = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='Completion Details']"))
                )
                completion_details_page.click()
                logger.info(f"Completion Details page clicked.")
            except TimeoutException as te:
                logger.error(f"Timed out waiting for Completion Details page: {te}")
            
            time.sleep(2)
            
            if completion_details_page:
                try:
                    completion_details=scrape_project_details.completion_details("Completion", "Details", self.driver)
                    logger.info(f"Completion Details 'completion_details' scrapped.")
                except Exception as e:
                    logger.warning(f"Completion Details 'completion_details' **not** scrapped.")

                try:
                    development_details_completion=scrape_project_details.col_md("completion", "Development", self.driver)
                    logger.info(f"Development Details 'development_details_completion' scrapped.")
                except Exception as e:
                    logger.warning(f"Development Details 'development_details_completion' **not** scrapped.")

                try:
                    uploaded_documents=scrape_project_details.col_md("completion", "Uploaded", self.driver)
                    logger.info(f"Uploaded Documents 'uploaded_documents' scrapped.")
                except Exception as e:
                    logger.warning(f"Uploaded Documents 'uploaded_documents' **not** scrapped.")

                try:
                    photos_uploaded=scrape_project_details.col_md("completion", "Photos", self.driver)
                    logger.info(f"Photos Uploaded 'photos_uploaded' scrapped.")
                except Exception as e:
                    logger.warning(f"Photos Uploaded 'photos_uploaded' **not** scrapped.")

            print(" ********************** Checking sheet is appending ********************** ")

            data_dict = {key: value if value is not None else "N/A" for key, value in {
                    'home_table_json': home_table_json,
                    'Promoter Details': promoter_details,
                    'Authorized Signatory Details': authorized_signatory_details,
                    'Project Member Details': project_member_details,
                    'Project Land Owner Details': project_land_owner_details,
                    'RERA Registration Details': rera_registration_details_with_any_details,
                    'Previous Project Details': previous_project_details,

                    'Project Details': project_details,
                    'Development Details': development_details,
                    'Project Ongoing Status': project_ongoing_status,
                    'External Development Work': external_development_work,
                    'Other External Development Work': other_external_development_work,
                    'Project Bank Details': project_bank_details,
                    'Project Agents': project_agents,
                    'Project Detail Table': project_detail_table,
                    'Project Documents': project_documents,
                    'Project Approval': project_approval,
                    'Declaration': declaration,
                    'Other Documents': other_documents,
                    'Project Photo': project_photo,
                    'Financial Document': financial_document,

                    "Promoter Table": promoter_table,
                    "Project Table": project_table,

                    'Completion Details': completion_details,
                    'Development Details': development_details_completion,
                    'Uploaded Documents': uploaded_documents,
                    'Photos Uploaded': photos_uploaded,
                }.items()}
            
            google_sheet_instance = Google_sheet_init()
            worksheet = google_sheet_instance.sheet()
            worksheet.append_rows([list(data_dict.values())], value_input_option="RAW")

        except TimeoutException as te:
            logger.error(f"Timeout occurred in scrape_project_details: {te}")
        except NoSuchElementException as ne:
            logger.error(f"Element not found in scrape_project_details: {ne}")
        except Exception as e:
            logger.error(f"An error occurred in scrape_project_details: {e}")
        
    def table_iter(self, page_num):

        project_details_button = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, f"//tbody/tr/td[4]"))
            )
        num_of_iter=len(project_details_button)+1

        for i in range(1, num_of_iter):
            print(f"************************************************ {i} Row iteration Started. ************************************************")

            SimpleTools.random_scroll(self.driver)

            home_table_json=self.view_project_details_table_process(i)
            self.scrape_project_details(home_table_json)
            time.sleep(2)

            try:
                checking_project_details = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, "//body/section[@id='site-content']/div[@class='pop_main']/div[@id='project_details_popup']/div[@class='modal-dialog-lg']/div[@class='modal-content']/div[@class='modal-body']/div[@id='result']/section[@id='site-content']/div[1]"))
                )
            except TimeoutException:
                logger.warning(f"Row {i} not clickable. Skipping...")
                checking_project_details=None

            if checking_project_details:
                logger.info(f"Project Details Page Detected.")
                self.driver.back()

                try:
                    project_details_button = WebDriverWait(self.driver, 2).until(
                            EC.element_to_be_clickable((By.XPATH, f"//tbody/tr[{i}]/td[4]"))
                        )
                except TimeoutException:
                    logger.warning(f"Table Disappeared")
                    project_details_button = None
                
                if not project_details_button:
                    self.city_selection()
                    time.sleep(2)

                SimpleTools.page_number_finder(page_num, self.driver)
                time.sleep(4)

            print(f"************************************************ {i} Row iteration completed. ************************************************")

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
                    logger.warning(f"No more pages available.")
                    break

            if page_num > 1:

                print("Page Num: ", page_num)
                next_button_element = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, f"//a[@class='paginate_button '][normalize-space(text())='{page_num}']"))
                )
                next_button_element.click()
                
                time.sleep(2)

            self.table_iter(page_num)

                


        








def main(city, headless_mode):
    scrapper = RERAScrapper(city, headless_mode)
    scrapper.initiailise_browers()
    scrapper.get_url()
    scrapper.city_selection()
    scrapper.page_iter()
    time.sleep(20000)


if __name__ == '__main__':
    main()