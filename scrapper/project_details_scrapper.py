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

    def col_md(page_name, xpath_text, driver, default_heading_one="Default Heading"):
        try:
            project_details = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"//div[@id='{page_name}']"))
            )

            h1_elements = project_details.find_element(By.XPATH, f"//div[@class='col-md-12' and contains(., '{xpath_text}')]")
            heading_one = h1_elements.text.strip() or default_heading_one
        except Exception as e:
            heading_one = default_heading_one  # Use the default value if extraction fails

        row_xpath = "./following-sibling::div[@class='row'][@style='font-size: 13px;']//div"
        rows = h1_elements.find_elements(By.XPATH, row_xpath)

        extracted_data = []

        for i in range(1, len(rows), 2):

            heading = h1_elements.find_element(By.XPATH, f"({row_xpath})[{i}]")
            content = h1_elements.find_element(By.XPATH, f"({row_xpath})[{i+1}]")

            heading=heading.text.strip().replace(":","")
            # content=content.text.strip()
            # Check if there's a link in the content element
            link_element = content.find_elements(By.TAG_NAME, "a")
            if link_element:
                content = link_element[0].get_attribute("href")
            else:
                content = content.text.strip()

            if not heading:
                continue

            extracted_data.append(f"{heading}: {content}")
            # print(f"{heading}: {content}")

        json_data = {
            heading_one: extracted_data
        }
        formatted_json = json.dumps(json_data, indent=4)
        return formatted_json
    
    def h1(page_name, heading_text1, heading_text2, driver, default_heading_one="Default Heading"):

        # project_details = WebDriverWait(driver, 20).until(
        #     EC.presence_of_element_located((By.XPATH, f"//div[@id='{page_name}']"))
        # )

        # # h1_elements = project_details.find_element(By.XPATH, f"//h1[@style='font-size: 16px;' and contains(., '{heading_text}')]")
        # h1_elements = project_details.find_element(By.XPATH, f"//h1[contains(., '{heading_text1}') and contains(., '{heading_text2}')]")

        # heading_one=h1_elements.text

        try:
            project_details = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"//div[@id='{page_name}']"))
            )

            h1_elements = project_details.find_element(By.XPATH, f"//h1[contains(., '{heading_text1}') and contains(., '{heading_text2}')]")
            heading_one = h1_elements.text.strip() or default_heading_one
        except Exception as e:
            heading_one = default_heading_one  # Use the default value if extraction fails

        row_xpath = "./following-sibling::div[@class='row'][@style='font-size: 13px;']//div"
        rows = h1_elements.find_elements(By.XPATH, row_xpath)

        extracted_data=[]

        for i in range(1, len(rows), 2):

            heading = h1_elements.find_element(By.XPATH, f"({row_xpath})[{i}]")
            content = h1_elements.find_element(By.XPATH, f"({row_xpath})[{i+1}]")
            
            heading=heading.text.strip().replace(":","")
            # content=content.text.strip()
            # Check if there's a link in the content element
            link_element = content.find_elements(By.TAG_NAME, "a")
            if link_element:
                content = link_element[0].get_attribute("href")
            else:
                content = content.text.strip()

            if not heading:
                continue

            extracted_data.append(f"{heading}: {content}")
            # print(f"{heading}: {content}")

        json_data = {
            heading_one: extracted_data
        }
        formatted_json = json.dumps(json_data, indent=4)
        return formatted_json

    def uploaded_doc_extractor (text1, text2, driver):
        # Wait for the project_details element
        project_details = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='menu2']"))
        )

        # Find all <h1> elements within the project_details element
        h1_elements = project_details.find_element(By.XPATH, f"//h1[contains(., '{text1}') and contains(., '{text2}')]")

        heading_one=h1_elements.text

        row_xpath = "./following-sibling::div[@class='row'][@style='font-size: 13px;']//div"
        rows = h1_elements.find_elements(By.XPATH, row_xpath)
        print(len(rows))

        extracted_data = []
        
        # Print the text of each row
        for i in range(1, len(rows), 2):
            try:
                heading_xpath = f"({row_xpath})[{i}]"
                content_xpath = f"({row_xpath})[{i+1}]"

                heading_element = h1_elements.find_element(By.XPATH, heading_xpath)
                content_element = h1_elements.find_element(By.XPATH, content_xpath)

                heading = heading_element.text.strip().replace(":", "")
                content = content_element.text.strip()

                link_element = content_element.find_element(By.TAG_NAME, "a")
                content_link = link_element.get_attribute("href") if link_element else "No link available"

                if not heading:
                    print(f"Skipped empty element at index {i-1}, {i}")
                    continue

                # Append formatted string to the list
                extracted_data.append(f"{heading}: {content_link}")

                # print(f"{heading}: {content}")
                # print("--------------------------------")
            except Exception as e:
                print(f"Error processing index {i-1}, {i}: {e}")

        # Convert extracted data to the desired JSON structure
        json_data = {
            heading_one: extracted_data
        }

        formatted_json = json.dumps(json_data, indent=4)
        print(formatted_json)

        # Optionally, return the JSON data for further processing
        return formatted_json


