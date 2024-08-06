import asyncio
from playwright.async_api import async_playwright
from database.database import Session
from database.repository import RedditPostRepository
from scrape.scraper_service import RedditScraperService

async def main():
    session = Session()
    repo = RedditPostRepository(session)
    scraper_service = RedditScraperService(repo)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        
        # Scrape multiple posts
        await scraper_service.scrape_multiple_posts(
            browser, 
            'https://www.reddit.com/r/ProRevenge/'
        )

        await browser.close()

    session.close()

if __name__ == "__main__":
    asyncio.run(main())