import argparse
import time

from dotenv import load_dotenv; load_dotenv()

from app.driver import DefaultWebDriver
from app.crawler import Reaper
from app.types.selector import CssSelector



parser = argparse.ArgumentParser(description="Online Shop scrapper with selenium")

parser.add_argument(
    "-n",
    "--name", 
    default="",
    required=False,
    dest="name",
    help="name of the scraper."
)

parser.add_argument(
    "--url", 
    required=False,
    dest="url",
    help="initial website url."
)

parser.add_argument(
    "--no_headless", 
    action="store_false", 
    default=True,
    dest="headless",
    help="run webdriver without headless mode."
)


options = parser.parse_args()


if __name__ == "__main__":
    # Create driver and crawler
    driver = DefaultWebDriver(headless=options.headless).create_driver()
    reaper = Reaper(driver=driver)

    # Crawl the webpage
    reaper.go_to_url("https://shopee.co.id")
    reaper.search("iphone13", CssSelector(".shopee-searchbar-input__input"))
    reaper.wait(3)
    reaper.scroll_until_bottom()
    search_item = reaper.get_elements(driver, CssSelector(".shopee-search-item-result__item"))
    product_names = reaper.get_elements_multi(search_item, CssSelector(".ie3A\+n.bM\+7UW.Cve6sh"))
    product_names = reaper.get_elements_text(product_names)
    
    print(product_names)

    reaper.quit()
    

#  tokopedia_crawler = MultiPageCrawler(
#         spider=tokopedia, 
#         pages=1, 
#         search_keyword="iphone 13",
#         search_bar=(By.CSS_SELECTOR, ".e110g5pc0"),
#         contents_parent=(By.CSS_SELECTOR, ".css-12sieg3"),
#         contents={
#             "name": (By.CSS_SELECTOR, ".css-1b6t4dn", pick_text()),
#             "price": (By.CSS_SELECTOR, ".css-1ksb19c", pick_text()),
#             "location": (By.CSS_SELECTOR, ".css-1kdc32b:nth-child(1)", pick_text()),
#             "shop": (By.CSS_SELECTOR, ".css-1kdc32b:nth-child(2)", pick_text()),
#             "link": (By.CSS_SELECTOR, "a", pick_attribute("href") )
#         }
#     )

# shopee_crawler = MultiPageCrawler(
#         spider=shopee, 
#         pages=1, 
#         search_keyword="iphone 13",
#         search_bar=(By.CSS_SELECTOR, ".shopee-searchbar-input__input"),
#         contents_parent=(By.CSS_SELECTOR, ".shopee-search-item-result__item"),
#         contents={
#             "name": (By.CSS_SELECTOR, ".ie3A\+n.bM\+7UW.Cve6sh", pick_text()),
#             "price": (By.CSS_SELECTOR, ".ZEgDH9", pick_text()),
#             "location": (By.CSS_SELECTOR, ".zGGwiV", pick_text()),
#             "link": (By.CSS_SELECTOR, "a", pick_attribute("href"))
#         }
#     )