from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random

class SimpleTools:

    def ava_page_number(driver):
        button_elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[@class='paginate_button ']"))
        )
        len(button_elements)

        pages = []
        for page_num in button_elements:
            page_num=page_num.text

            pages.append(page_num)

        return pages

    def largest_page_number(driver):

        pages = SimpleTools.ava_page_number(driver)

        largest_num = 0
        for page in pages:
            if int(page) > int(largest_num):
                largest_num=page

        largest_num=int(largest_num)

        return largest_num

    def second_largest_number(pages):
        numbers = [int(num) for num in pages]

        largest = float('-inf')  
        second_largest = float('-inf')

        for num in numbers:
            if num > largest:
                second_largest = largest
                largest = num
            elif num > second_largest and num != largest:
                second_largest = num

        return second_largest
    
    def page_number_finder(page_num, driver):

        pages = SimpleTools.ava_page_number(driver)
        second_largest=SimpleTools.second_largest_number(pages)
        # print(f"{page_num} : {second_largest}")

        while page_num > second_largest:
            try:
                next_page_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f"//a[@class='paginate_button '][normalize-space(text())='{second_largest}']")))
                next_page_button.click()
                second_largest += 1
                time.sleep(2)
            except TimeoutException:
                print("No more pages available.")
                break

        if page_num > 1:

            next_button_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"//a[@class='paginate_button '][normalize-space(text())='{page_num}']"))
            )
            next_button_element.click()
            
            time.sleep(1)

    def random_scroll(driver):
        random_integer = random.randint(0, 4)
        for _ in range(random_integer):
            
            random_integer = random.randint(5, 8)
            for _ in range(random_integer):
                
                # Execute JavaScript to scroll down
                random_number = random.uniform(600, 800)
                driver.execute_script(f"window.scrollBy(0, {random_number});")
                
                # Wait for the content to load if applicable
                random_number = random.uniform(0, 1)
                time.sleep(random_number)