from olshop_scrapper.scrapper import TokopediaScrapper


class Application:
    def start(self):
        scrapper = TokopediaScrapper(headless=False)
        scrapper.find_product("laptop asus")
        scrapper.driver.quit()


if __name__ == "__main__":
    app = Application()
    app.start()