from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

class LinkScraper:
    def __init__(self, chrome_driver_path, url,user_data_dir):
        self.chrome_driver_path = chrome_driver_path
        self.url = url
        self.user_data_dir = user_data_dir
        self.driver = None


    def get_links(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f"user-data-dir={self.user_data_dir}")
        chrome_options.add_argument("--headless")  
        self.driver = webdriver.Chrome(service=Service(self.chrome_driver_path), options=chrome_options)

        try:
            self.driver.get(self.url)
            self.driver.implicitly_wait(2)

            ul_element = self.driver.find_element(By.XPATH, '//*[@id="rw-menutop"]/li[1]/div/ul')
            soup = BeautifulSoup(ul_element.get_attribute('outerHTML'), 'html.parser')

            links = set()

            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']

                if href == "javaScript:void(0);":
                    continue

                parts = href.split("/")
                if len(parts) == 6:
                    links.add(href)

            sorted_links = sorted(list(links))
            print("Scraped Links:", sorted_links)  
            return sorted_links 
        finally:
            self.driver.quit()

