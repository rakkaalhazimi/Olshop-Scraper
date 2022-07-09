import csv
import json
import time
from typing import Tuple, Dict, List
from urllib.parse import urlparse, parse_qs, urlencode

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from driver import create_options
from driver import create_driver


Locator = Tuple[str, str]
Contents = Dict[str, Locator]


class Spider:
    def __init__(self, headless: bool = True):
        self.head = create_options(headless=headless)
        self.driver = create_driver("chromedriver.exe", options=self.head)
        self.wait = WebDriverWait(self.driver, 5)
        self.action = ActionChains(self.driver)


    def search(self, keyword: str, locator: Locator):
        try: 
            # Wait then find search bar
            search_bar = self.wait.until(
                EC.presence_of_element_located(locator)
            )
            search_bar.clear() # search bar ga mau diclear
            search_bar.send_keys(keyword)
            search_bar.send_keys(Keys.ENTER)

        except (TimeoutException, NoSuchElementException) as e:
            print("time out. Koneksi Internetmu mungkin lambat. Error: searchbar/search button")
            self.driver.quit()


    def scroll_infinitely(self):
        """_summary_

        ref: https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
        """
        SCROLL_PAUSE_TIME = 0.5

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
        SCROLL_PAUSE_TIME = 0.5
        SCROLL_TRIES = 3

        # Select html tag
        html = self.driver.find_element(By.TAG_NAME, "html")

        new_diff = -1
        

        while SCROLL_TRIES > 1:
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Press page down on browser
            html.send_keys(Keys.PAGE_DOWN)

            # Get current height after scroll
            last_height = self.driver.execute_script("return window.pageYOffset")

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            last_diff = new_height - last_height

            if new_diff == last_diff:
                SCROLL_TRIES -= 1

            new_diff = last_diff

    

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
    
    def quit(self):
        return self.driver.quit()
            



class Tokopedia(Spider):
    
    def __init__(self, url: str, **kwargs):
        super().__init__(**kwargs)
        self.url = self.driver.get(url)

    def snapshot(self):
        return self.driver.save_screenshot("tokopedia.png")


class Shopee(Spider):
    
    def __init__(self, url: str, **kwargs):
        super().__init__(**kwargs)
        self.url = self.driver.get(url)

    def snapshot(self):
        return self.driver.save_screenshot("shopee.png")


if __name__ == "__main__":
    tokopedia = Tokopedia(
        url="https://www.tokopedia.com/", 
        headless=False,
    )
    tokopedia.search("iphone 13", locator=(By.CSS_SELECTOR, ".e110g5pc0"))
    tokopedia.scroll_until_bottom()
    time.sleep(1)
    tokopedia.redirect_next_page(page=2)
    time.sleep(1)
    tokopedia.snapshot()
    tokopedia.quit()

    # shopee = Shopee(
    #     url="https://shopee.co.id/", 
    #     headless=False,
    # )
    # shopee.search("iphone 13", locator=(By.CSS_SELECTOR, ".shopee-searchbar-input__input"))
    # shopee.scroll_until_bottom()
    # shopee.click_next_page((By.CSS_SELECTOR, ".shopee-icon-button.shopee-icon-button--right"))
    # shopee.scroll_until_bottom()
    # shopee.click_next_page((By.CSS_SELECTOR, ".shopee-icon-button.shopee-icon-button--right"))
    # shopee.scroll_until_bottom()
    # time.sleep(2)
    # shopee.snapshot()
    # shopee.quit()


