from typing import List

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from app.types.selector import Selector



class ReaperCollector:
    def get_element(self, element: WebDriver or WebElement, selector: Selector):
        return element.find_element(selector.by, selector.value)

    def get_elements(self, element: WebDriver or WebElement, selector: Selector):
        return element.find_elements(selector.by, selector.value)

    def get_element_attr(self, element: WebElement, key: str):
        return element.get_attribute(key)

    def get_elements_attr(self, elements: List[WebElement], key: str):
        return [element.get_attribute(key) for element in elements]

    def get_elements_multi(self, elements: List[WebElement], selector: Selector):
        return [element.find_element(selector.by, selector.value) for element in elements]

    def get_element_text(self, element: WebElement):
        return element.text

    def get_elements_text(self, elements: List[WebElement]):
        return [element.text for element in elements]

    
