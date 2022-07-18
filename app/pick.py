from functools import partial
from selenium.webdriver.remote.webelement import WebElement


def pick_text():
    def _pick_text(tag: WebElement):
        return tag.text
    return partial(_pick_text)

def pick_attribute(attr: str):
    def _pick_attribute(tag: WebElement, attr: str):
        return tag.get_attribute(attr)
    return partial(_pick_attribute, attr=attr)