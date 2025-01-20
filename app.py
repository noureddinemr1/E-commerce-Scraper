from flask import Flask, jsonify, request
import asyncio
import os
import chromedriver_autoinstaller
from LinkScraper import LinkScraper
from Scraper import Scraper

app = Flask(__name__)

# Automatically install chromedriver
chromedriver_autoinstaller.install()  # This will install the correct chromedriver version

# Endpoint to start scraping process
@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()

    # Check if URL is provided in the request body
    if not data or not data.get('url'):
        return jsonify({"error": "URL is required"}), 400

    url = data['url']
    chromedriver_path = os.getenv('CHROMEDRIVER_PATH', '/chromedriver.exe')

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
            scraper = Scraper(links)
            scraped_data = scraper.scrape_all()
            return scraped_data
        except Exception as e:
            return {"error": str(e)}

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    scraped_data = loop.run_until_complete(run_scraper())

    # Handle errors in scraping process
    if "error" in scraped_data:
        return jsonify({"error": scraped_data["error"]}), 500

    return jsonify(scraped_data), 200

# Main function to test locally
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)
