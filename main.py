import argparse
import os

from dotenv import load_dotenv; load_dotenv()
from selenium.webdriver.common.by import By

from app.crawler import MultiPageCrawler
from app.driver import DefaultWebDriver
from app.mongo import connect_cluster
from app.pick import pick_text, pick_attribute
from app.spider import Spider

parser = argparse.ArgumentParser(description="Online Shop scrapper with selenium")

parser.add_argument(
    "--headless", action="store_true", default=True, help="run webdriver with headless mode (default)")
parser.add_argument(
    "--no_headless", action="store_false", dest="headless", help="run webdriver without headless mode")


args = parser.parse_args()


if __name__ == "__main__":
    mongo_client = connect_cluster(os.getenv("mongo_user"), os.getenv("mongo_pass"))
    driver = DefaultWebDriver(headless=args.headless).create_driver()

    # Tokopedia
    tokopedia = Spider(
        name="Tokopedia",
        url="https://www.tokopedia.com/", 
        driver=driver,
        mongo_client=mongo_client
    )

    tokopedia_crawler = MultiPageCrawler(
        spider=tokopedia, 
        pages=1, 
        search_keyword="iphone 13",
        search_bar=(By.CSS_SELECTOR, ".e110g5pc0"),
        contents_parent=(By.CSS_SELECTOR, ".css-12sieg3"),
        contents={
            "name": (By.CSS_SELECTOR, ".css-1b6t4dn", pick_text()),
            "price": (By.CSS_SELECTOR, ".css-1ksb19c", pick_text()),
            "location": (By.CSS_SELECTOR, ".css-1kdc32b:nth-child(1)", pick_text()),
            "shop": (By.CSS_SELECTOR, ".css-1kdc32b:nth-child(2)", pick_text()),
            "link": (By.CSS_SELECTOR, "a", pick_attribute("href") )
        }
    )

    tokopedia_crawler.execute()

    # Shopee
    shopee = Spider(
        name="Shopee",
        url="https://shopee.co.id/", 
        driver=driver,
        mongo_client=mongo_client
    )

    shopee_crawler = MultiPageCrawler(
        spider=shopee, 
        pages=1, 
        search_keyword="iphone 13",
        search_bar=(By.CSS_SELECTOR, ".shopee-searchbar-input__input"),
        contents_parent=(By.CSS_SELECTOR, ".shopee-search-item-result__item"),
        contents={
            "name": (By.CSS_SELECTOR, ".ie3A\+n.bM\+7UW.Cve6sh", pick_text()),
            "price": (By.CSS_SELECTOR, ".ZEgDH9", pick_text()),
            "location": (By.CSS_SELECTOR, ".zGGwiV", pick_text()),
            "link": (By.CSS_SELECTOR, "a", pick_attribute("href"))
        }
    )

    shopee_crawler.execute()