from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import json

class scrape_project_details:

    def col_md(page_name, xpath_text, driver):

        project_details = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f"//div[@id='{page_name}']"))
        )

        h1_elements = project_details.find_element(By.XPATH, f"//div[@class='col-md-12' and contains(., '{xpath_text}')]")
        heading_one=h1_elements.text

        row_xpath = "./following-sibling::div[@class='row'][@style='font-size: 13px;']//div"
        rows = h1_elements.find_elements(By.XPATH, row_xpath)

        extracted_data = []

        for i in range(1, len(rows), 2):

            heading = h1_elements.find_element(By.XPATH, f"({row_xpath})[{i}]")
            content = h1_elements.find_element(By.XPATH, f"({row_xpath})[{i+1}]")

            heading=heading.text.strip().replace(":","")
            content=content.text.strip()

            if not heading:
                continue

            extracted_data.append(f"{heading}: {content}")
            # print(f"{heading}: {content}")

        json_data = {
            heading_one: extracted_data
        }
        formatted_json = json.dumps(json_data, indent=4)
        return formatted_json
    
    def h1(page_name, heading_text, driver):

        project_details = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f"//div[@id='{page_name}']"))
        )

        h1_elements = project_details.find_element(By.XPATH, f"//h1[@style='font-size: 16px;' and contains(., '{heading_text}')]")

        heading_one=h1_elements.text

        row_xpath = "./following-sibling::div[@class='row'][@style='font-size: 13px;']//div"
        rows = h1_elements.find_elements(By.XPATH, row_xpath)

        extracted_data=[]

        for i in range(1, len(rows), 2):

            heading = h1_elements.find_element(By.XPATH, f"({row_xpath})[{i}]")
            content = h1_elements.find_element(By.XPATH, f"({row_xpath})[{i+1}]")
            
            heading=heading.text.strip().replace(":","")
            content=content.text.strip()

            if not heading:
                continue

            extracted_data.append(f"{heading}: {content}")
            # print(f"{heading}: {content}")

        json_data = {
            heading_one: extracted_data
        }
        formatted_json = json.dumps(json_data, indent=4)
        return formatted_json

