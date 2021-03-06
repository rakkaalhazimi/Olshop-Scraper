import platform
from typing import Tuple, List
from selenium.webdriver import chrome
from selenium import webdriver

OS_NAME = platform.system()
LINUX_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
WIN_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"


class DefaultWebDriver:
    def __init__(self, headless: bool):
        options = webdriver.ChromeOptions()

        # Headless mode
        if headless:
            options.add_argument("--headless")

        # User agent
        if OS_NAME == "Windows":
            options.add_argument(f"user-agent={WIN_USER_AGENT}")
        else:
            options.add_argument(f"user-agent={LINUX_USER_AGENT}")

        # Default options
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')

        # Instantiate webdriver
        self._driver = webdriver.Chrome(options=options)

    def create_driver(self):
        return self._driver


if __name__ == "__main__":
    driver = DefaultWebDriver(headless=True).create_driver()
    driver.quit()
