import argparse

parser = argparse.ArgumentParser(description="Online Shop scrapper with selenium")
parser.add_argument("--no-headless", action="store_true", help="run webdriver without headless mode")

args = parser.parse_args()