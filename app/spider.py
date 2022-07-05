import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from driver import create_options
from driver import create_driver


class Spider:
    def __init__(self, headless: bool = True):
        self.head = create_options(headless=headless)
        self.driver = create_driver("chromedriver.exe", options=self.head)
        self.wait = WebDriverWait(self.driver, 5)

    def scroll_infinitely(self):
        """_summary_

        ref: https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
        """
        SCROLL_PAUSE_TIME = 0.5

        while True:
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Get scroll height
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height


    def scroll_until_bottom(self):
        """_summary_
        ref: https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
        """
        SCROLL_PAUSE_TIME = 0.5
        SCROLL_TRIES = 2

        # Select html tag
        html = self.driver.find_element(By.TAG_NAME, "html")

        new_diff = -1
        

        while SCROLL_TRIES > 1:
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Press page down on browser
            html.send_keys(Keys.PAGE_DOWN)

            # Get current height after scroll
            last_height = self.driver.execute_script("return window.pageYOffset")

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            last_diff = new_height - last_height

            print(new_diff, last_diff)
            if new_diff == last_diff:
                SCROLL_TRIES -= 1

            new_diff = last_diff

    

    def click_next_page(self):
        ...
            



class Tokopedia(Spider):
    
    def __init__(self, url: str, **kwargs):
        super().__init__(**kwargs)
        self.url = self.driver.get(url)

    def search(self, keyword: str):
        try: 
            # Wait then find search bar
            search_bar = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".e110g5pc0")))
            search_bar.clear() # search bar ga mau diclear
            search_bar.send_keys(keyword)

            # find submit button
            search_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".css-1czin5k")))
            search_button.click()

        except (TimeoutException, NoSuchElementException) as e:
            print("time out. Koneksi Internetmu mungkin lambat. Error: searchbar/search button")
            self.driver.quit()

    def snapshot(self):
        return self.driver.save_screenshot("tokopedia.png")
    
    def quit(self):
        return self.driver.quit()


class Shopee(Spider):
    
    def __init__(self, url: str, **kwargs):
        super().__init__(**kwargs)
        self.url = self.driver.get(url)

    def search(self, keyword: str):
        try: 
            # Wait then find search bar
            search_bar = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".shopee-searchbar-input__input")))
            search_bar.clear() # search bar ga mau diclear
            search_bar.send_keys(keyword)

            # find submit button
            search_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".shopee-searchbar__search-button")))
            search_button.click()

        except (TimeoutException, NoSuchElementException) as e:
            print("time out. Koneksi Internetmu mungkin lambat. Error: searchbar/search button")
            self.driver.quit()

    def snapshot(self):
        return self.driver.save_screenshot("shopee.png")
    
    def quit(self):
        return self.driver.quit()


if __name__ == "__main__":
    # tokopedia = Tokopedia(
    #     url="https://www.tokopedia.com/p/handphone-tablet/handphone", 
    #     headless=False,
    # )
    # tokopedia.search("iphone 13")
    # tokopedia.scroll_until_bottom()
    # tokopedia.snapshot()
    # tokopedia.quit()

    shopee = Shopee(
        url="https://shopee.co.id/", 
        headless=False,
    )
    shopee.search("iphone 13")
    shopee.scroll_until_bottom()
    shopee.snapshot()
    shopee.quit()


