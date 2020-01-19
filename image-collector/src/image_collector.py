import os
import json
import urllib.request as urllib
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class GoogleImageCollector:
    def __init__(self, project, subclass, search_term, max_images, username=None, headless=True):
        self.headless = headless
        self.max_images = max_images
        self.search_term = search_term
        self.counter = 0
        self.success_counter = 0
        self.browser = self.build_selenium_browser()
        if username:
            self.data_path = os.path.join('/','data', username, project, 'data', subclass)
        else:
            self.data_path = os.path.join('/', 'data', project, 'data', subclass)
        if not os.path.exists(self.data_path):
            os.makedirs(os.path.join(self.data_path))

    def build_url(self):
        return "https://www.google.co.in/search?q=" + self.search_term + "&source=lnms&tbm=isch"

    def build_selenium_browser(self):
        options = Options()
        if self.headless:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')

        browser = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", chrome_options=chrome_options)
        return browser

    def collect_images(self):
        url = self.build_url()

        self.browser.get(url)

        for _ in range(500):
            self.browser.execute_script("window.scrollBy(0,10000)")

            for x in self.browser.find_elements_by_xpath('//div[contains(@class,"rg_meta")]'):
                self.counter += 1
                print("Total Count:", self.counter)
                print("Succsessful Count:", self.success_counter)
                print("URL:", json.loads(x.get_attribute('innerHTML'))["ou"])
                img = json.loads(x.get_attribute('innerHTML'))["ou"]
                img_type = json.loads(x.get_attribute('innerHTML'))["ity"]
                try:
                    raw_img = urllib.urlopen(img, timeout=5).read()
                except Exception as e:
                    print("Failed to download image", e)

                try:
                    if len(img_type) == 0:
                        f = open(os.path.join(self.data_path, "img" + "_" + str(self.success_counter) + ".jpg"), 'wb')
                    else:
                        f = open(os.path.join(self.data_path, "img" + "_" + str(self.success_counter) + "." + img_type), 'wb')
                    f.write(raw_img)
                    f.close()
                    self.success_counter += 1
                except Exception as e:
                    print("Failed Persisting Image", e)

                if self.success_counter >= self.max_images:
                    break

            if self.success_counter >= self.max_images:
                break

        print(self.success_counter, "pictures succesfully downloaded")

        self.browser.close()



