from typing import Mapping, Tuple, Any

from requests import PreparedRequest
from selenium import webdriver
from selenium.webdriver.common.by import By



class MultiPageSpider:
    """Crawl and scrap element from multiple pages in website."""

    def __init__(self,
                 driver: webdriver.Chrome,
                 address: str,
                 pages: int,
                 ):
        """
        _summary_

        Args:
            driver (webdriver.Chrome): chrome webdriver (preferebly)
            address (str): target address
            pages (int): number of pages
        """
        self.driver = driver
        self.address = address
        self.pages = pages

    def __len__(self):
        return self.pages

    def __iter__(self):
        return (self.__getitem__(i) for i in range(self.pages))

    def __getitem__(self, pos) -> Mapping[str, Any]:
        page = pos + 1

        # Prepare url
        req = PreparedRequest()
        params = {"page": page}
        req.prepare_url(self.address, params)

        # Visit link
        self.driver.get(req.url)

        # Get elements

        return {"page": page, "status": "success", "url": req.url}



if __name__ == "__main__":
    spider = MultiPageSpider(driver=None, address="https://google.com", pages=2)
    for response in iter(spider):
        print(response)