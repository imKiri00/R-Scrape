import asyncio
from scrape.scraper_main import main as scraper_main
#from evaluation.evaluation_main import main as evaluation_main

async def main():
    await scraper_main()
    #await evaluation_main()

if __name__ == "__main__":
    asyncio.run(main())