from typing import List

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from app.core import ReaperCollector, ReaperNavigator, ReaperExporter
from app.types.selector import Selector



class Reaper:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.navigator = ReaperNavigator(driver)
        self.exporter = ReaperExporter()
        self.collector = ReaperCollector()

    def click(self, selector: Selector):
        self.navigator.click(selector)

    def get_element(self, element: WebDriver or WebElement, selector: Selector):
        return self.collector.get_element(element, selector)

    def get_elements(self, element: WebDriver or WebElement, selector: Selector):
        return self.collector.get_elements(element, selector)

    def get_element_attr(self, element: WebElement, key: str):
        return self.collector.get_element_attr(element, key)

    def get_elements_attr(self, elements: List[WebElement], key: str):
        return self.collector.get_elements_attr(elements, key)

    def get_elements_multi(self, elements: List[WebElement], selector: Selector):
        return self.collector.get_elements_multi(elements, selector)

    def get_element_text(self, element: WebElement):
        return self.collector.get_element_text(element)

    def get_elements_text(self, elements: List[WebElement]):
        return self.collector.get_elements_text(elements)

    def go_to_url(self, url):
        self.navigator.go_to_url(url)

    def redirect_next_page(self):
        self.navigator.redirect_next_page()

    def search(self, keyword: str, selector: Selector):
        self.navigator.search(keyword, selector)

    def scroll_infinitely(self):
        self.navigator.scroll_infinitely()

    def scroll_until_bottom(self):
        self.navigator.scroll_until_bottom()

    def scroll_with_steps(self, steps: int):
        self.navigator.scroll_with_steps(steps)

    def snapshot(self, filename: str = None):
        self.navigator.snapshot(filename)

    def quit(self):
        self.navigator.quit()

    def wait(self, seconds):
        self.navigator.implicit_wait(seconds)