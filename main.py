import argparse

from app.driver import DefaultWebDriver

parser = argparse.ArgumentParser(description="Online Shop scrapper with selenium")

parser.add_argument(
    "--headless", action="store_true", default=True, help="run webdriver with headless mode (default)")
parser.add_argument(
    "--no_headless", action="store_false", dest="headless", help="run webdriver without headless mode")


args = parser.parse_args()


if __name__ == "__main__":
    driver = DefaultWebDriver(headless=args.headless).create_driver()
    driver.get("https://google.com")
    driver.save_screenshot("google.png")