import os
import json
import urllib.request as urllib
from selenium import webdriver


class GoogleImageCollector:
    def __init__(self, project, subclass, search_term, max_images, username, visited_urls):
        self.max_images = max_images
        self.search_term = search_term
        self.visited_urls = visited_urls
        self.counter = 0
        self.success_counter = 0
        self.collected_image_urls = []
        self.browser = self._build_selenium_browser()
        self.data_path = os.path.join('/','data', username, project, 'data', subclass)
        if not os.path.exists(self.data_path):
            os.makedirs(os.path.join(self.data_path))

    def build_url(self):
        return "https://www.google.co.in/search?q=" + self.search_term + "&source=lnms&tbm=isch"

    @staticmethod
    def _build_selenium_browser():
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

            for x in self.browser.find_elements_by_xpath('//img[contains(@class,"rg_i")]'):
                print(x)
                self.counter += 1
                print("Total Count:", self.counter)
                print("Succsessful Count:", self.success_counter)

                img = x.get_attribute('data-iurl')
                print(img)
                if img in self.visited_urls:
                    continue

                try:
                    raw_img = urllib.urlopen(img, timeout=5).read()
                except Exception as e:
                    print("Failed to download image", e)

                try:
                    f = open(os.path.join(self.data_path, "img" + "_" + str(self.success_counter + len(self.visited_urls)) + ".jpg"), 'wb')

                    f.write(raw_img)
                    f.close()
                    self.success_counter += 1
                    self.collected_image_urls.append(img)
                except Exception as e:
                    print("Failed Persisting Image", e)

                if self.success_counter >= self.max_images:
                    break

            if self.success_counter >= self.max_images:
                break

        print(self.success_counter, "pictures successfully downloaded")

        self.browser.close()
        return self.collected_image_urls



