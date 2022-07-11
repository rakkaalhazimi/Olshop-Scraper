from selenium.webdriver.common.by import By

from app.driver import DefaultWebDriver
from app.spider import Spider, Contents, Locator


class Crawler:
    def execute(self):
        return NotImplementedError("Cannot call directly on superclass, please call on subclass")


class MultiPageCrawler(Crawler):
    def __init__(
            self, 
            spider: Spider, 
            pages: int, 
            search_keyword: str = "", 
            search_bar: Locator = None,
            contents_parent: Locator = None,
            contents: Contents = None
        ):
        self.spider = spider
        self.pages = pages
        self.search_keyword = search_keyword
        self.search_bar = search_bar
        self.contents_parent = contents_parent
        self.contents = contents


    def execute(self):

        self.spider.start()

        if self.search_bar:
            self.spider.search(self.search_keyword, self.search_bar)

        try:
            for page in range(2, self.pages + 2):
                self.spider.driver.implicitly_wait(1)
                self.spider.scroll_until_bottom()

                if self.contents_parent and self.contents:
                    records = self.spider.grab_by_parent(
                        parent=self.contents_parent,
                        contents=self.contents
                    )
                    self.spider.to_json(f"record_{page - 1}", records=records)

                self.spider.redirect_next_page(page=page)

        finally:
            self.spider.quit()
