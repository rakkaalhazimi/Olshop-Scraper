import platform
from typing import Tuple, List
from selenium.webdriver import chrome
from selenium import webdriver

OS_NAME = platform.system()
LINUX_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
WIN_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"

def create_options(
        headless: bool = True,
        resolution: Tuple[int, int] = (1920, 1080),
    ):

    options = webdriver.ChromeOptions()
    width, height = resolution

    if headless:
        options.add_argument("--headless")

    if OS_NAME == "Linux":
        options.add_argument(f"user-agent={LINUX_USER_AGENT}")
    else:
        options.add_argument(f"user-agent={WIN_USER_AGENT}")
    
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


def create_driver(
        path: str = None,
        options: chrome.options.Options = None
    ):

    driver = webdriver.Chrome(path, options=options)
    return driver


if __name__ == "__main__":
    options = create_options(headless=False, resolution=(1366, 768))
    driver = create_driver(options=options)
    driver.get("https://google.com")
    driver.save_screenshot("google.png")
    driver.quit()