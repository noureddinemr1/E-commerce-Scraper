# Web Scraper Project

This project is a web scraper designed to scrape product information from a specific e-commerce website. It fetches links, creates folder structures, and scrapes products based on those links, saving them in JSON format.

## Features
- **Link Scraping**: Extracts links from a predefined URL.
- **Folder Structure Creation**: Creates a folder structure for categories and departments based on the scraped links.
- **Product Scraping**: Scrapes product information (name and price) from product pages, supporting pagination.
- **Data Saving**: Saves scraped product data into JSON files for further use.

## Requirements

This project requires the following Python libraries:

- `requests`: For making HTTP requests to fetch web pages.
- `beautifulsoup4`: For parsing and extracting data from HTML content.
- `lxml`: A parser for faster HTML parsing.

You can install the required libraries using the provided `requirements.txt`.

### Install Dependencies

1. Clone the repository or download the project files.
2. Install the required Python libraries by running the following command:

   ```bash
   pip install -r requirements.txt

#### Run

3. Run index.py and wait the result.

## Test it on postman : 
   ```bash
   http://localhost:5000/scrape