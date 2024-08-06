from flask import Flask, jsonify
import asyncio
from dotenv import load_dotenv
from shared.database.database import Session
from shared.database.repository import RedditPostRepository
from story_evaluator import StoryEvaluator
import os

load_dotenv()

app = Flask(__name__)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    asyncio.run(run_evaluation())
    return jsonify({"message": "Evaluation completed"}), 200

async def run_evaluation():
    session = Session()
    repo = RedditPostRepository(session)
    evaluator = StoryEvaluator(api_key=os.environ.get('GROQ_API_KEY'))
    
    unevaluated_posts = repo.get_unrated_posts()
    
    evaluated_count = 0
    for post in unevaluated_posts:
        rating = await evaluator.evaluate_story(post)
        if rating is not None:
            post.rating = rating
            repo.update(post)
            print(f"Evaluated post {post.id} with rating {rating}")
            evaluated_count += 1
        else:
            print(f"Failed to evaluate post {post.id}")
    
    session.close()
    print(f"Evaluation completed. Evaluated {evaluated_count} posts.")

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)