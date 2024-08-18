# R-Scrape

R-Scrape is a Reddit scraping project that uses Playwright to automate web browsing, extract data from Reddit posts, and evaluate the content using AI models.

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
├── evaluation_pipeline/
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── groq.py
│   │   ├── llama.py
│   │   └── ollama.py
│   ├── __init__.py
│   ├── config.py
│   └── main.py
└── ui/
    ├── app.py
    ├── database_view.py
    └── docker_management.py
```

## Features

- Scrapes Reddit posts from specified subreddits
- Uses Playwright for web automation
- Stores scraped data in a database
- Evaluates Reddit posts using AI models
- Provides a user interface for viewing and managing scraped data

## Dependencies

```
streamlit==1.37.1
pandas==2.2.2
requests==2.32.3
Flask==3.0.3
SQLAlchemy==2.0.32
playwright==1.45.1
beautifulsoup4==4.12.3
psycopg2-binary==2.9.9
transformers==4.37.2
torch==2.2.0
```

## Usage

### Reddit Scraping

The main script (`Playwright/main.py`) demonstrates how to use the Reddit scraper:

1. It initializes the database connection.
2. Creates a RedditPostRepository and RedditScraperService.
3. Launches a Playwright browser instance.
4. Scrapes multiple posts from the specified subreddit (in this case, 'r/ProRevenge').

### Post Evaluation

The evaluation pipeline (`evaluation_pipeline/main.py`) allows you to evaluate scraped Reddit posts using various AI providers:

1. Run the script with the desired AI provider:
   ```
   python evaluation_pipeline/main.py --provider [llama|ollama|groq]
   ```
2. The script will fetch unevaluated posts from the database, evaluate them using the specified AI provider, and update the database with the evaluation scores.

## User Interface

The project includes a user interface for viewing and managing the scraped data. To run the UI:

1. Go to the root folder.
2. Run the following command:
   ```
   streamlit run ui/app.py
   ```

## Configuration

Make sure to set up the `config.yaml` file with the necessary database and AI provider configurations before running the scripts.
