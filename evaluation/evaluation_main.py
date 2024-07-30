import asyncio
import os
from database.database import Session
from database.repository import RedditPostRepository
from evaluation.story_evaluator import StoryEvaluator

async def main():
    session = Session()
    repo = RedditPostRepository(session)
    evaluator = StoryEvaluator(api_key=os.environ.get('GROQ_API_KEY'))

    # Get unevaluated posts directly from the database
    unevaluated_posts = repo.get_unevaluated_posts()
    
    for post in unevaluated_posts:
        rating = await evaluator.evaluate_story(post)
        post.rating = rating
        repo.update(post)
        print(f"Evaluated post {post.id} with rating {rating}")

    session.close()

if __name__ == "__main__":
    asyncio.run(main())