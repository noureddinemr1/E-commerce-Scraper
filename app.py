from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import chromedriver_autoinstaller
from LinkScraper import LinkScraper
from Scraper import Scraper

app = FastAPI()

chromedriver_path = chromedriver_autoinstaller.install()
os.environ["PATH"] += os.pathsep + os.path.dirname(chromedriver_path)

class ScrapeRequest(BaseModel):
    url: str

@app.post("/scrape")
async def scrape(data: ScrapeRequest):
    url = data.url

    try:
        link_scraper = LinkScraper(chrome_driver_path=chromedriver_path, url=url)
        links = link_scraper.get_links()

        if not links:
            raise HTTPException(status_code=404, detail="No links found")

        scraper = Scraper(links)
        scraped_data = scraper.scrape_all()
        return scraped_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
