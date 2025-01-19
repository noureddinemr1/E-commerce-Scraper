import requests
from bs4 import BeautifulSoup
import json
import os

class Scraper:
    def __init__(self, links_file):
        self.links_file = links_file
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})
    
    def scrape_page(self, url):
        response = self.session.get(url)
        products = []
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')

            product_list = soup.find('ol', class_='products list items product-items')
            if product_list:
                items = product_list.find_all('li', class_='product-item')
                for item in items:
                    product_name = item.find('strong', class_='product name product-item-name')
                    product_price = item.find('span', class_='price')
                    if product_name and product_price:
                        products.append({
                            'product_name': product_name.text.strip(),
                            'product_price': product_price.text.strip()
                        })
        else:
            print(f"Failed to fetch page: {url}")
        return products

    def scrape_element(self, department_name, category_name, item_name, base_url):
        page_num = 1
        all_products = []
        first_page_products = None

        while True:
            url = f"{base_url}?p={page_num}"
            products_on_page = self.scrape_page(url)
            if page_num == 1:
                first_page_products = products_on_page
            if not products_on_page or (page_num > 1 and products_on_page == first_page_products):
                break
            all_products.extend(products_on_page)
            print(f"Scraped page {page_num} for {item_name} in {department_name}/{category_name}.")
            page_num += 1

        if all_products:
            department_folder = os.path.join(department_name)
            category_folder = os.path.join(department_folder, category_name)
            os.makedirs(category_folder, exist_ok=True)

            filename = os.path.join(category_folder, f"{item_name}.json")
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(all_products, f, ensure_ascii=False, indent=4)
            print(f"Data for {item_name} in {department_name}/{category_name} saved to {filename}")
        else:
            print(f"No products found for {item_name} in {category_name}/{department_name}.")

    def parse_links(self):
        with open(self.links_file, 'r') as file:
            links = json.load(file)
        return links

    def scrape_all(self):
        links = self.parse_links()

        for link in links:
            link_parts = link.split("/")
            department_name = link_parts[3]
            category_name = link_parts[4]
            item_name = link_parts[5]

            self.scrape_element(department_name, category_name, item_name, link)
