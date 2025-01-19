import asyncio
import os
from LinkScraper import LinkScraper
from FolderStructureCreator import FolderStructureCreator
from Scraper import Scraper

async def main():
    # Define the path to the chromedriver (assuming it's in the same folder as this script)
    chromedriver_path = os.path.join(os.getcwd(), 'chromedriver.exe')  # This will automatically point to the current directory
    
    # Update PATH environment variable
    current_path = os.environ.get('PATH', '')
    os.environ['PATH'] = current_path + os.pathsep + chromedriver_path

    # Create LinkScraper object and run it
    link_scraper = LinkScraper(
        chrome_driver_path=chromedriver_path,  # Use the path to chromedriver
        url="https://www.mytek.tn"
    )
    link_scraper.get_links()

    # Create FolderStructureCreator object and run it
    folder_creator = FolderStructureCreator("links.json")
    folder_creator.create_folder_structure()

    # Create Scraper object and run it with a concurrency limit of 50
    scraper = Scraper('links.json')
    await scraper.scrape_all()

# Run the main function
asyncio.run(main())
