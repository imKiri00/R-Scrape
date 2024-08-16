# R-Scrape

R-Scrape is a Reddit scraping project that uses Playwright to automate web browsing, extract data from Reddit posts and more.

## Project Structure

```
R-Scrape/
├── Playwright/
│   ├── database.py
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── main.py
│   ├── repository.py
│   ├── requirements.txt
│   └── service.py
├── UI/
└── ui/
    ├── app.py
    ├── database_view.py
    └── docker_management.py
```

## Features

- Scrapes Reddit posts from specified subreddits
- Uses Playwright for web automation
- Stores scraped data in a database
- Provides a user interface for viewing and managing scraped data

## Dependencies

```
- playwright==1.46.0
- asyncpg
- sqlalchemy[asyncio]
- psycopg2-binary
- beautifulsoup4
- lxml
```

## Usage

The main script (`Playwright/main.py`) demonstrates how to use the Reddit scraper:

1. It initializes the database connection.
2. Creates a RedditPostRepository and RedditScraperService.
3. Launches a Playwright browser instance.
4. Scrapes multiple posts from the specified subreddit (in this case, 'r/ProRevenge').

## User Interface

The project includes a user interface for viewing and managing the scraped data. To run the UI:
Go to root folder and run the following:

```
streamlit run ui/app.py
```
