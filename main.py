import argparse
import time

from selenium.webdriver.common.by import By

from app.crawler import MultiPageCrawler
from app.driver import DefaultWebDriver
from app.spider import Spider

parser = argparse.ArgumentParser(description="Online Shop scrapper with selenium")

parser.add_argument(
    "--headless", action="store_true", default=True, help="run webdriver with headless mode (default)")
parser.add_argument(
    "--no_headless", action="store_false", dest="headless", help="run webdriver without headless mode")


args = parser.parse_args()


if __name__ == "__main__":
    driver = DefaultWebDriver(headless=args.headless).create_driver()
    # driver.get("https://google.com")
    # driver.save_screenshot("google.png")

    tokopedia = Spider(
        name="Tokopedia",
        url="https://www.tokopedia.com/", 
        driver=driver,
    )

    tokopedia_crawler = MultiPageCrawler(
        spider=tokopedia, 
        pages=1, 
        search_keyword="iphone 13",
        search_bar=(By.CSS_SELECTOR, ".e110g5pc0"),
        contents_parent=(By.CSS_SELECTOR, ".css-12sieg3"),
        contents={
            "name": (By.CSS_SELECTOR, ".css-1b6t4dn"),
            "price": (By.CSS_SELECTOR, ".css-1ksb19c"),
            "location": (By.CSS_SELECTOR, ".css-1kdc32b:nth-child(1)"),
            "shop": (By.CSS_SELECTOR, ".css-1kdc32b:nth-child(2)"),
            "link": (By.CSS_SELECTOR, "a")
        }
    )

    # tokopedia_crawler.execute()


    shopee = Spider(
        name="Shopee",
        url="https://shopee.co.id/", 
        driver=driver,
    )

    shopee_crawler = MultiPageCrawler(
        spider=shopee, 
        pages=1, 
        search_keyword="iphone 13",
        search_bar=(By.CSS_SELECTOR, ".shopee-searchbar-input__input"),
        contents_parent=(By.CSS_SELECTOR, ".shopee-search-item-result__item"),
        contents={
            "name": (By.CSS_SELECTOR, ".ie3A\+n.bM\+7UW.Cve6sh"),
            "price": (By.CSS_SELECTOR, ".ZEgDH9"),
            "location": (By.CSS_SELECTOR, ".zGGwiV"),
            "link": (By.CSS_SELECTOR, "a")
        }
    )

    shopee_crawler.execute()