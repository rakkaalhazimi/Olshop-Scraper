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
        }
    )

    tokopedia_crawler.execute()


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