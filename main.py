import asyncio
from scrape.scraper_main import main as scraper_main
from evaluation.evaluation_main import main as evaluation_main

async def pipeline():
    # Scraping stage
    #await scraper_main()
    
    # Evaluation stage
    await evaluation_main()
    
    # Add other stages here as needed

if __name__ == "__main__":
    asyncio.run(pipeline())