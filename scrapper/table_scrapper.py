from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import json

class TableScrapper:

    def home_table_extractor(driver):
        enter_username = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//tbody/tr[2]")))
        html_content=enter_username.get_attribute("outerHTML")
        # print(html_content)
        return html_content

    def extract_home_table(html_content):

        html_content = TableScrapper.home_table_extractor()

        soup = BeautifulSoup(html_content, "html.parser")
        row = soup.find("tr")
        headers = [
            "S.No",
            "ACKNOWLEDGEMENT NO",
            "REGISTRATION NO",
            "View Project Details",
            "PROMOTER NAME",
            "PROJECT NAME",
            "STATUS",
            "DISTRICT",
            "TALUK",
            "PROJECT TYPE",
            "APPROVED ON",
            "PROPOSED COMPLETION DATE",
            "PROPOSED COMPLETION DATE AT THE TIME OF REGISTRATION",
            "COVID-19 EXTENSION DATE",
            "SECTION 6 EXTENSION DATE",
            "FURTHER EXTENSION DATE",
            "Certificate",
            "Covid Certificate",
            "Renewed Certificate",
            "FURTHER EXTENSION ORDER",
            "COMPLAINTS / LITIGATION",
        ]

        data = []
        for cell in row.find_all("td"):
            text = cell.get_text(strip=True)
            link = cell.find("a")
            if link and link.get("href"):
                text = link["href"]
            data.append(text)

        json_data = {headers[i]: data[i] if i < len(data) else "" for i in range(len(headers))}
        return json.dumps(json_data, indent=4)

    # json_output = extract_table_row_to_json(html_content)
    # print(json_output)
