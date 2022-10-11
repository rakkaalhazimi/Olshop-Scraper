import json
import os
import time
from typing import Dict, List

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from app.utils.url import get_url_query, set_url_query
from app.utils.filepath import make_dir
from app.types.selector import Selector


MONGO_DATABASE = "Olshop"
SCRAP_DIR = "scrap_results"
SCROLL_PAUSE_TIME = 0.5


class ReaperNavigator:
    """
    Main feature of scrapper application, it crawls and picks data from website page.

    """
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 5)
        self.action = ActionChains(self.driver)

    def click(self, selector: Selector):
        """
        Click selected element in the current page.

        Args:
            selector (Selector): element to be clicked

        """
        button = self.driver.find_element(selector.by, selector.value)
        button.click()

    def go_to_url(self, url):
        """
        Go to the destinated url.

        """
        self.driver.get(url)

    def implicit_wait(self, seconds):
        time.sleep(seconds)

    def quit(self):
        return self.driver.quit()

    def redirect_next_page(self):
        """
        Redirect current page into the next page by using "page" query.

        """
        current_url = self.driver.current_url
        current_page = get_url_query(current_url, "page") or 1
        next_page_url = set_url_query(current_url, "page", int(current_page) + 1)
        self.go_to_url(next_page_url)

    def search(self, keyword: str, selector: Selector):
        """
        Search any keyword from located search bar.

        Args:
            keyword (str): search query
            selector (Selector): search bar selector

        """
        try:
            # Wait then find search bar
            search_bar = self.wait.until(
                EC.presence_of_element_located((selector.by, selector.value))
            )
            search_bar.clear()
            search_bar.send_keys(keyword)
            search_bar.send_keys(Keys.ENTER)

        except (TimeoutException, NoSuchElementException):
            print("Request timeout - Your internet connection is slow")
            self.driver.quit()

    def scroll_infinitely(self):
        """
        Scroll the current page endlessly.

        reference: 
        https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python

        """
        while True:
            time.sleep(SCROLL_PAUSE_TIME)
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            last_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )
            if new_height == last_height:
                break
            else:
                last_height = new_height

    def scroll_until_bottom(self):
        """
        Scroll until the bottom of current page.

        reference: 
        https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python

        """
        scroll_tries = 3
        new_diff = -1

        while scroll_tries > 1:
            time.sleep(SCROLL_PAUSE_TIME)
            self.action.send_keys(Keys.PAGE_DOWN).perform()
            last_height = self.driver.execute_script(
                "return window.pageYOffset"
            )
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )
            last_diff = new_height - last_height

            if new_diff == last_diff:
                scroll_tries -= 1
            else:
                new_diff = last_diff

    def scroll_with_steps(self, steps: int):
        """
        Scroll for n steps.

        Args:
            steps (int): how many scroll are performed
        """
        for _ in range(steps):
            self.action.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(SCROLL_PAUSE_TIME)

    def snapshot(self, filename: str = None):
        """
        Take a screenshot of the current visited page.

        Args:
            filename (str, optional): image filename. Defaults to None.

        Returns:
            _type_: _description_
        """
        return self.driver.save_screenshot(f"{filename or self.name}.png")

    def to_json(self, fn: str, records: List[Dict]):
        make_dir(SCRAP_DIR)
        dir_ = os.path.join(SCRAP_DIR, self.name)
        make_dir(dir_)

        # Write records to json
        path_ = os.path.join(dir_, fn)
        with open(f"{path_}.json", "w") as file:
            json_string = json.dumps(records)
            file.write(json_string)

    def to_mongo_cluster(self, records: List[Dict]):
        database = self.mongo_client[MONGO_DATABASE]
        collection = database[self.name]
        return collection.insert_many(records)
