from app.driver import get_driver, get_options
from app.spider import MultiPageSpider


if __name__ == "__main__":
    address = "https://www.tokopedia.com/p/handphone-tablet/handphone"
    options = get_options(headless=False)
    driver = get_driver(options=options)

    spider = MultiPageSpider(driver=driver, address=address, pages=2)

    for response in spider:
        print(response)