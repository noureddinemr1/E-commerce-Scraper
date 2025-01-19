from flask import Flask, jsonify, request
import asyncio
import os
from LinkScraper import LinkScraper
from Scraper import Scraper

app = Flask(__name__)

# Endpoint to start scraping process
@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()

    if not data or not data.get('url'):
        return jsonify({"error": "URL is required"}), 400

    url = data['url']
    chromedriver_path = os.path.join(os.getcwd(), 'chromedriver.exe')

    # Add chromedriver to the PATH
    os.environ['PATH'] = os.environ.get('PATH', '') + os.pathsep + chromedriver_path

    async def run_scraper():
        try:
            # Initialize the LinkScraper and scrape links
            link_scraper = LinkScraper(chrome_driver_path=chromedriver_path, url=url)
            links = link_scraper.get_links()

            if not links:
                return {"error": "No links found"}

            # Initialize the Scraper and scrape all
            scraper = Scraper(links)  # Pass links directly
            scraped_data = scraper.scrape_all()  # Call scrape_all synchronously
            return scraped_data
        except Exception as e:
            return {"error": str(e)}


    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    scraped_data = loop.run_until_complete(run_scraper())

    if "error" in scraped_data:
        return jsonify({"error": scraped_data["error"]}), 500

    return jsonify(scraped_data), 200


if __name__ == '__main__':
    app.run(debug=True)
