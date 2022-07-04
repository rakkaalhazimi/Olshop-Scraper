from app.driver import create_driver, create_options
from app.spider import MultiPageSpider


if __name__ == "__main__":
    address = "https://www.tokopedia.com/p/handphone-tablet/handphone"
    options = create_options(headless=False)
    driver = create_driver(options=options)

    spider = MultiPageSpider(driver=driver, address=address, pages=2)

    for response in spider:
        print(response)