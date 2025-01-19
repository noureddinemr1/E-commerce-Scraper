import asyncio
from LinkScraper import LinkScraper
from FolderStructureCreator import FolderStructureCreator
from Scraper import Scraper

async def main():
    link_scraper = LinkScraper(
        chrome_driver_path="C:/Users/noure/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe",
        url="https://www.mytek.tn"
    )
    link_scraper.get_links()

    scraper = Scraper(links_file="links.json")
    scraper.scrape_all()

    scraper = Scraper(concurrency_limit=50)  
    await scraper.scrape('links.json')

asyncio.run(main())
