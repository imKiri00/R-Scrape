import asyncio
from playwright.async_api import async_playwright
from database import init_db, AsyncSessionLocal
from repository import RedditPostRepository
from service import RedditScraperService


async def main():
    await init_db()
    
    async with AsyncSessionLocal() as session:
        repo = RedditPostRepository(session)
        scraper_service = RedditScraperService(repo)

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)

            await scraper_service.scrape_multiple_posts(
                browser,
                'https://www.reddit.com/r/ProRevenge/'
            )

            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())