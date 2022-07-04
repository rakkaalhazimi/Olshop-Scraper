from typing import Tuple, List
from selenium.webdriver import chrome
from selenium import webdriver


def get_options(
        headless: bool = True,
        resolution: Tuple[int, int] = (1920, 1080),
    ):

    options = webdriver.ChromeOptions()
    width, height = resolution

    if headless:
        options.add_argument("--headless")
    options.add_argument(f"--window-size={width},{height}")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')

    return options


def get_driver(
        path: str = "chromedriver.exe",
        options: chrome.options.Options = None
    ):

    driver = webdriver.Chrome(path, options=options)
    return driver


if __name__ == "__main__":
    options = get_options(headless=False, resolution=(1366, 768))
    driver = get_driver(options=options)
    driver.get("https://google.com")
    driver.save_screenshot("google.png")
    driver.quit()