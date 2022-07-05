from driver import get_driver
from driver import get_options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Olshop:

    def __init__(self):
        self.head = get_options(headless=True) # kalau false baru bisa
        self.driver = get_driver("chromedriver.exe", options=self.head)
        self.wait = WebDriverWait(self.driver, 5)


class Tokopedia(Olshop):
    
    def __init__(self, url):
        super().__init__()
        self.url = self.driver.get(url)

    def search(self, keyword):
    # Wait then find search bar
        try: 
            search_bar = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".e110g5pc0")))
            search_bar.clear() # search bar ga mau diclear
            search_bar.send_keys(keyword)

    #find submit button
            search_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".css-1czin5k")))
            search_button.click()
        except:
            print("time out. Koneksi Internetmu mungkin lambat. Error: searchbar/search button")
            self.driver.quit()

    def snapshot(self):
        return self.driver.save_screenshot("tokopedia.png")
    
    def quit(self):
        return self.driver.quit()


class Shopee(Olshop):
    pass


tokopedia = Tokopedia(url = "https://tokopedia.com")

tokopedia
tokopedia.search("iphone 13")
tokopedia.snapshot()
tokopedia.quit()




