from flask import Flask
import asyncio
from scraper_service import RedditScraperService
from shared.database.database import Session, create_tables
from shared.database.repository import RedditPostRepository
from playwright.async_api import async_playwright

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    asyncio.run(main())
    return "Scraping completed", 200

async def main():
    create_tables()
    session = Session()
    repo = RedditPostRepository(session)
    scraper_service = RedditScraperService(repo)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        await scraper_service.scrape_multiple_posts(
            browser, 
            'https://www.reddit.com/r/ProRevenge/'
        )
        await browser.close()

    session.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)