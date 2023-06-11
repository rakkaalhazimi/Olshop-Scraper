from abc import ABC, abstractmethod
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from olshop_scrapper.driver import DefaultWebDriver


class Scrapper(ABC):
    def __init__(self, headless: bool = True):
        self.driver = DefaultWebDriver(headless=headless).get_driver()
        self.driver.implicitly_wait(2)
        self.action = ActionChains(self.driver)

    def scroll_until_bottom(self):
        scroll_tries = 3
        new_diff = -1
        while scroll_tries > 1:
            time.sleep(0.5)
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

    @abstractmethod
    def find_product(self, name: str):
        ...


class TokopediaScrapper(Scrapper):
    def find_product(self, name: str):
        self.driver.get("https://www.tokopedia.com/")

        # Enter product name
        search_field = self.driver.find_element(By.XPATH, "//input[@class='css-3017qm exxxdg63']")
        search_field.send_keys(name)
        search_field.send_keys(Keys.ENTER)
        time.sleep(1)

        # Scroll until bottom
        self.scroll_until_bottom()