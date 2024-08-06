import groq
from database.models import RedditPost

class StoryEvaluator:
    def __init__(self, api_key):
        self.client = groq.AsyncClient(api_key=api_key)

    async def evaluate_story(self, post: RedditPost) -> float:
        prompt = f"""
        Rate the following story on a scale from 0 (extremely boring) to 10 (highly entertaining):

        Title: {post.headline}
        
        Story:
        {post.content}

        Provide a single number between 0 and 10 as your rating, with no additional text.
        """

        chat_completion = await self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
            max_tokens=10,
        )

        try:
            rating = float(chat_completion.choices[0].message.content.strip())
            return min(max(rating, 0), 10)  # Ensure rating is between 0 and 10
        except ValueError:
            print(f"Error parsing rating for post {post.id}")
            return None