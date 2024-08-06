import asyncio
import os
from dotenv import load_dotenv
import aiohttp

load_dotenv()

SCRAPER_URL = os.getenv('SCRAPER_URL', 'http://scraper:8000')
EVALUATOR_URL = os.getenv('EVALUATOR_URL', 'http://evaluation:8000')

async def trigger_scraper(max_retries=5, delay=5):
    async with aiohttp.ClientSession() as session:
        for attempt in range(max_retries):
            try:
                async with session.post(f"{SCRAPER_URL}/scrape") as response:
                    if response.status == 200:
                        print("Scraping completed successfully")
                        return
                    else:
                        print(f"Scraping failed with status {response.status}")
                        print(await response.text())
            except aiohttp.ClientConnectorError as e:
                print(f"Connection failed. Retrying in {delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                print(f"Error: {str(e)}")
                await asyncio.sleep(delay)
        print("Max retries reached. Scraping failed.")

async def trigger_evaluator(max_retries=5, delay=5):
    async with aiohttp.ClientSession() as session:
        for attempt in range(max_retries):
            try:
                async with session.post(f"{EVALUATOR_URL}/evaluate") as response:
                    if response.status == 200:
                        print("Evaluation completed successfully")
                        return
                    else:
                        print(f"Evaluation failed with status {response.status}")
                        print(await response.text())
            except aiohttp.ClientConnectorError as e:
                print(f"Connection failed. Retrying in {delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                print(f"Error: {str(e)}")
                await asyncio.sleep(delay)
        print("Max retries reached. Evaluation failed.")

async def main():
    print("Starting orchestration process...")
    
    print("Triggering scraper...")
    await trigger_scraper()
    
    print("Triggering evaluator...")
    await trigger_evaluator()
    
    print("Orchestration process completed.")

if __name__ == "__main__":
    asyncio.run(main())