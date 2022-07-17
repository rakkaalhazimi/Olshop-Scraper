import csv
import json
import os
import time
from tqdm import tqdm
from typing import Tuple, Dict, List
from urllib.parse import urlparse, parse_qs, urlencode

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


Locator = Tuple[str, str]
Contents = Dict[str, Locator]
SCRAP_DIR = "scrap_results"
SCROLL_PAUSE_TIME = 0.5



class Spider:
    def __init__(self, name: str, url: str, driver: WebDriver):
        self.driver = driver
        self.name = name
        self.url = url
        self.wait = WebDriverWait(self.driver, 5)
        self.action = ActionChains(self.driver)

    def start(self):
        self.driver.get(self.url)

    def search(self, keyword: str, locator: Locator):
        try: 
            # Wait then find search bar
            search_bar = self.wait.until(
                EC.presence_of_element_located(locator)
            )
            search_bar.clear() # search bar ga mau diclear
            search_bar.send_keys(keyword)
            search_bar.send_keys(Keys.ENTER)

        except TimeoutException:
            print("[ERROR] Request timeout - Your internet connection is slow")
            self.driver.quit()

        except NoSuchElementException:
            print("[ERROR] Element not found - No search bar found")
            self.driver.quit()



    def scroll_infinitely(self):
        """_summary_

        ref: https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
        """

        while True:
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Get scroll height
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height


    def scroll_until_bottom(self):
        """_summary_
        ref: https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
        """
        SCROLL_TRIES = 3

        new_diff = -1

        while SCROLL_TRIES > 1:
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Press page down on browser
            self.action.send_keys(Keys.PAGE_DOWN).perform()

            # Get current height after scroll
            last_height = self.driver.execute_script("return window.pageYOffset")

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            last_diff = new_height - last_height

            if new_diff == last_diff:
                SCROLL_TRIES -= 1

            new_diff = last_diff

    def scroll_with_steps(self, steps: int):
        # pause time & inet speed berpengaruh thd maximum data yang direcord
        # harusnya max 80(+3)produk/page
        
        for down in range(0, steps):
            self.action.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(SCROLL_PAUSE_TIME)


    def grab(self, content: Contents):
        return

    
    def grab_by_parent(self, parent: Locator, contents: Contents):
        records = []
        parent_tags = self.driver.find_elements(*parent)
        for p_tag in parent_tags:
            row = {}
            for column, child in contents.items():
                c_tag = p_tag.find_element(*child)
                row[column] = c_tag.text
            records.append(row)
            
        return records


    def click_next_page(self, locator: Locator):
        next_button = self.driver.find_element(*locator)
        return next_button.click()


    def redirect_next_page(self, page: int):
        # Get current url
        current_url = self.driver.current_url

        # Parse url
        parsed_url = urlparse(current_url)

        # Parse query and assign new page
        query_dict = parse_qs(parsed_url.query)
        query_dict["page"] = page

        # Encode query
        new_query = urlencode(query_dict, doseq=True)

        # Replace query with the newer one
        new_url = parsed_url._replace(query=new_query).geturl()
        
        # Redirect to next page
        self.driver.get(new_url)


    def snapshot(self):
        return self.driver.save_screenshot("browser.png")


    def to_csv(self, data: str):
        COLUMNS = ["Name", "Price", "Shop","Location"]  # write header
        # create csv file
        try:
            with open("result.csv", "w", newline="", encoding="utf-8") as write:
                write = csv.writer(write)
                write.writerow(COLUMNS)
        finally:
            with open("result.csv", "a", newline="", encoding="utf-8") as write:
                write = csv.writer(write)
                write.writerows(data)


    def to_json(self, fn: str, records: List[Dict]):
        
        # Create dir if not exists
        dir_ = os.path.join(SCRAP_DIR, self.name)
        if not os.path.exists(dir_):
            os.mkdir(SCRAP_DIR)
            os.mkdir(dir_)

        # Write records to json
        path_ = os.path.join(dir_, fn)
        with open(f"{path_}.json", "w") as file:
            json_string = json.dumps(records)
            file.write(json_string)


    def snapshot(self, filename: str = None):
        return self.driver.save_screenshot(f"{filename or self.name}.png")
    
    def quit(self):
        return self.driver.quit()
