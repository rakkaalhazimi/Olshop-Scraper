import platform
import requests
import os
import zipfile
from selenium import webdriver


OS_NAME = platform.system()
LINUX_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
WIN_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
CHROMEDRIVER_FILENAME = "chromedriver.exe"


def get_chrome_latest_release():
    url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    response = requests.request("GET", url)
    return response.text

def write_response_stream(filename, response):
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            # Filter out to keep alive-new chunks
            if chunk:  
                f.write(chunk)

def extract_one(zipFn, targetFn):
    with zipfile.ZipFile(zipFn) as zip_file:
        zip_file.extract(targetFn)


def download_latest_chrome():
    latest_ver = get_chrome_latest_release()
    url = f"https://chromedriver.storage.googleapis.com/{latest_ver}/chromedriver_win32.zip"
    zip_filename = url.split("/")[-1]
    response = requests.get(url, stream=True)  # Stream allow for immediate download
    write_response_stream(zip_filename, response)
    return zip_filename


def update_webdriver():
    # Stop if webdriver exists or the os isn't windows
    if os.path.exists(CHROMEDRIVER_FILENAME) or OS_NAME != "Windows":
        return
    else:
        zip_filename = download_latest_chrome()
        os.remove(zip_filename)


class DefaultWebDriver:
    def __init__(self, headless: bool):
        options = webdriver.ChromeOptions()

        # Update webdriver
        update_webdriver()

        if headless:
            options.add_argument("--headless")

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

        self._driver = webdriver.Chrome(options=options)

    def create_driver(self):
        return self._driver


if __name__ == "__main__":
    driver = DefaultWebDriver(headless=True).create_driver()
    driver.quit()
