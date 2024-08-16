from datetime import datetime
from playwright.async_api import Page, Browser
from bs4 import BeautifulSoup
import re
from lxml import etree
import asyncio
from database import RedditPost
from repository import RedditPostRepository

MAX_INSTANCES = 5  # 1 main + 4 additional

class RedditScraperService:
    def __init__(self, repository: RedditPostRepository):
        self.repository = repository

    async def scrape_multiple_posts(self, browser: Browser, subreddit_url: str):
        main_page = await browser.new_page()
        await main_page.goto(subreddit_url)
        await main_page.wait_for_selector('shreddit-app', timeout=30000)

        post_pages = []
        post_number = 1
        scroll_attempts = 0
        max_scroll_attempts = 5

        while True:
            if len(post_pages) < MAX_INSTANCES - 1:
                post_href = await main_page.evaluate(f"""
                    () => {{
                        let postLink = document.evaluate(
                            '/html/body/shreddit-app/div/div[1]/div[2]/main/div[2]/shreddit-feed/article[{post_number}]/shreddit-post/a[1]',
                            document,
                            null,
                            XPathResult.FIRST_ORDERED_NODE_TYPE,
                            null
                        ).singleNodeValue;
                        
                        if (!postLink) {{
                            postLink = document.evaluate(
                                '/html/body/shreddit-app/div/div[1]/div[2]/main/div[2]/shreddit-feed/faceplate-batch/article[{post_number}]/shreddit-post/a[1]',
                                document,
                                null,
                                XPathResult.FIRST_ORDERED_NODE_TYPE,
                                null
                            ).singleNodeValue;
                        }}
                        
                        return postLink ? postLink.href : null;
                    }}
                """)

                if not post_href:
                    if scroll_attempts < max_scroll_attempts:
                        print(f"No post found at position {post_number}. Scrolling down...")
                        await main_page.evaluate("window.scrollBy(0, window.innerHeight)")
                        await asyncio.sleep(2)
                        scroll_attempts += 1
                        continue
                    else:
                        print(f"No more posts found after {scroll_attempts} scroll attempts")
                        break

                scroll_attempts = 0
                post_page = await browser.new_page()
                post_pages.append(post_page)
                
                await post_page.goto(post_href)
                await post_page.wait_for_selector('shreddit-post', timeout=10000)

                content = await post_page.content()
                soup = BeautifulSoup(content, 'lxml')

                headline = soup.select_one('shreddit-post h1')
                headline_text = headline.text.strip() if headline else 'Headline not found'

                dom = etree.HTML(str(soup))
                post_content = dom.xpath('/html/body/shreddit-app/div/div[1]/div/main/shreddit-post/div[2]')
                post_text = ' '.join(post_content[0].itertext()).strip() if post_content else 'Content not found'
                post_text = re.sub(r'\s+', ' ', post_text).strip()

                post = RedditPost(
                    headline=headline_text,
                    content=post_text,
                    url=post_href,
                    created_at=datetime.now(),
                    rating=None,
                    llm_evaluation=None
                )
                await self.repository.add(post)
                await self.repository.commit()  # Commit the changes to the database

                print(f"Post {post_number} Headline: {headline_text}")
                print(f"Post {post_number} Content: {post_text[:500]}...")
                print(f"Post {post_number} saved to database.")

                asyncio.create_task(self.close_page_after_delay(post_page, post_number, 5))

                post_number += 1
            else:
                await asyncio.sleep(1)
                post_pages = [page for page in post_pages if not page.is_closed()]

        await asyncio.sleep(30)
        await main_page.close()

    async def close_page_after_delay(self, page, post_number, delay):
        await asyncio.sleep(delay)
        await page.close()
        print(f"Closed post {post_number}")