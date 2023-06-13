from abc import ABC, abstractmethod
from typing import List, Mapping
import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from olshop_scrapper.driver import DefaultWebDriver
from olshop_scrapper.model import TokopediaProductModel


class Scrapper(ABC):
    def __init__(self, headless: bool = True):
        self.driver = DefaultWebDriver(headless=headless).get_driver()
        self.driver.implicitly_wait(2)
        self.action = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 2)

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

    def use_search_bar(self, keyword: str, xpath: str):
        search_field = self.wait.until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        search_field.clear()
        search_field.send_keys(keyword)
        search_field.send_keys(Keys.ENTER)
        time.sleep(2)

    @abstractmethod
    def find_product(self, name: str, pages: int) -> List[Mapping[str, str]]:
        ...


class TokopediaScrapper(Scrapper):
    def find_product(self, name: str, pages: int = 1) -> List[Mapping[str, str]]:
        self.driver.get("https://www.tokopedia.com/")
        self.use_search_bar(name, "//input[@class='css-3017qm exxxdg63']")
        self.scroll_until_bottom()

        current_page = 0
        products = []

        while current_page < pages:
            block_elements = self.wait.until(
                EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='css-llwpbs']"))
            )

            for block in block_elements:
                inner_html = block.get_attribute("innerHTML")
                soup = BeautifulSoup(inner_html, "html.parser")

                url = soup.select_one("div.css-1f2quy8 > a")
                if url:
                    url = url.attrs.get("href")

                image_url = soup.select_one("img.css-1q90pod")
                if image_url:
                    image_url = image_url.attrs.get("src")

                pname = soup.select_one("div[data-testid='spnSRPProdName']")
                if pname:
                    pname = pname.text

                place = soup.select_one("span[data-testid='spnSRPProdTabShopLoc']")
                if place:
                    place = place.text

                seller = soup.select_one("div.css-1rn0irl > span:nth-child(2)")
                if seller:
                    seller = seller.text

                current_price = soup.select_one("div[data-testid='spnSRPProdPrice']")
                if current_price:
                    current_price = current_price.text

                previous_price = soup.select_one("div[data-testid='lblProductSlashPrice']")
                if previous_price:
                    previous_price = previous_price.text

                rating = soup.select_one("span.prd_rating-average-text.css-t70v7i")
                if rating:
                    rating = rating.text

                sold = soup.select_one("span.prd_label-integrity.css-1duhs3e")
                if sold:
                    sold = sold.text

                trait = soup.select_one("div[aria-label='price label']")
                if trait:
                    trait = trait.text

                product = TokopediaProductModel(
                    url=url,
                    image_url=image_url,
                    name=pname,
                    place=place,
                    seller=seller,
                    current_price=current_price,
                    previous_price=previous_price,
                    rating=rating,
                    sold=sold,
                    trait=trait
                )
                products.append(product.to_dict())

            next_page_button = self.driver.find_element(By.XPATH, "//button[@aria-label='Laman berikutnya']")
            next_page_button.click()
            current_page += 1
            time.sleep(1)

        return products