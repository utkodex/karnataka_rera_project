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

    def home_table_json(driver):

        html_content = TableScrapper.home_table_extractor(driver)

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
    
    def financial_document_extractor(driver):
        fin_document = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//div[@id='menu2']//div[contains(@class,'inner_wrapper')]//div//table[contains(@class,'table-condensed')]")))
        html_content=fin_document.get_attribute("outerHTML")
        return html_content

    def financial_document_json_creator(driver):

        html_content=TableScrapper.financial_document_extractor(driver)
        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        table = soup.find("table", {"class": "table-condensed"})

        # Get table headers
        headers = [header.get_text(strip=True) for header in table.find("tr").find_all("th")]

        # Get table rows
        data_rows = table.find_all("tr")[1:]  # Skip the header row

        # Extract data into a structured format
        data = {}
        for row in data_rows:
            cols = row.find_all("td")
            row_title = cols[0].get_text(strip=True)  # Row title (e.g., Balance Sheet)
            row_data = {}
            for i, col in enumerate(cols[1:]):  # Skip the first column (row name)
                link = col.find("a")
                if link:
                    row_data[headers[i + 1]] = {
                        "name": link.get_text(strip=True),
                        "url": link["href"]
                    }
            data[row_title] = row_data

        # Convert the data to JSON
        json_data = json.dumps(data, indent=4)

        # Output the JSON
        return json_data
    
    def project_detail_table_extractor(driver):
        project_detail_table_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"(//tbody)[2]")))
        html_content=project_detail_table_element.get_attribute("outerHTML")
        return html_content

    def project_detial_table_json_creator(driver):

        html_content=TableScrapper.project_detail_table_extractor(driver)

        soup = BeautifulSoup(html_content, "html.parser")
        row = soup.find("tr")
        headers = [
            "stage",
            "start_date",
            "end_date",
            "certificate_link",
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
