from selenium.webdriver.common.by import By

class Selector:
    by: str
    value: str

class CssSelector(Selector):
    def __init__(self, value):
        self.by = By.CSS_SELECTOR
        self.value = value

class XpathSelector(Selector):
    def __init__(self, value):
        self.by = By.XPATH
        self.value = value

class ClassSelector(Selector):
    def __init__(self, value):
        self.by = By.CLASS_NAME
        self.value = value

class IdSelector(Selector):
    def __init__(self, value):
        self.by = By.ID
        self.value = value
    