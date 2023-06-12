import json

from olshop_scrapper.scrapper import TokopediaScrapper


class Application:
    def start(self):
        scrapper = TokopediaScrapper(headless=True)
        products = scrapper.find_product("laptop asus", pages=2)

        with open("result.jsonl", "w") as file:
            for product in products:
                file.write(json.dumps(product))
                file.write("\n")

        scrapper.driver.quit()


if __name__ == "__main__":
    app = Application()
    app.start()