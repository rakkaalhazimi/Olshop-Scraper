import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
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
        self.action = ActionChains(self.driver)

    def scroll(self, steps: str):
        SCROLL_PAUSE_TIME = 2 # ini dan speed inet bisa pengaruh ke jumlah data yang dikoleksi
        #jika speed inet lemot, scroll time bisa dinaikkan supaya jumlah data ditampilkan maximal

        for down in range(0, steps):
            self.action.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(SCROLL_PAUSE_TIME)
            

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

        except TimeoutException:
            print("time out. Koneksi Internetmu mungkin lambat.")
            self.driver.quit()
        except NoSuchElementException:
            print("Search bar error.")
            self.driver.quit()

    def grab(self, name: bool=True, price: bool=True, 
                    shop: bool=True, location: bool=True ):

        #location_ contain shop name and shop location
        name_, price_, location_ = [],[],[]

        if name is True:
            product_names = self.driver.find_elements_by_class_name("css-1b6t4dn") #pake css selector error
            for product_name in product_names:
                name_.append(product_name.text)

        if price is True:
            product_prices = self.driver.find_elements_by_class_name("css-1ksb19c")
            for product_price in product_prices:
                price_.append(product_price.text)

        if shop is True:
            try: # produk rekomendasi tidak punya location_
                recomended_prod = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".css-kkkpmy")))#css selector box produk rekomendasi
                for rec in recomended_prod:
                    location_.append("-")
                    location_.append("-")
        # mendata semua lokasi produk
            finally:
                product_locations = self.driver.find_elements_by_class_name("css-1kdc32b")
                for product_location in product_locations:
                    location_.append(product_location.text)
        
        # Memisahkan data toko dengan data daerah
        shop_name = []
        city_location = []
        city_locs_index = 0
        shop_locs_index = 0

        #city location terletak di baris ganjil dari list location_
        for loc in location_:
            city_locs_index += 1
            if city_locs_index % 2 == 1:
                city_location.append(location_[city_locs_index - 1])
            else:
                continue
        #shop name terletak di baris genap dari list location_
        for location in location_:
            shop_locs_index += 1
            if shop_locs_index % 2 == 0:
                shop_name.append(location_[shop_locs_index - 1])
            else:
                continue

        print(f'''name{name_}={len(name_)}\n, 
        price{price_}={len(price_)}\n, 
        shop name{shop_name}={len(shop_name)}\n,
        city location{city_location}={len(city_location)}''') 
        #total data cuma 18 produk, harusnya 80, max produk 80/page
        # kemungkinan ada masalah di scroll()


    def snapshot(self):
        return self.driver.save_screenshot("tokopedia.png")
    
    def quit(self):
        return self.driver.quit()


class Shopee(Spider):
    pass


if __name__ == "__main__":
    tokopedia = Tokopedia(url="https://www.tokopedia.com/p/handphone-tablet/handphone", headless=True)
    tokopedia.search("iphone 13")
    tokopedia.scroll(10)
    tokopedia.grab()
    tokopedia.snapshot()
    tokopedia.quit()