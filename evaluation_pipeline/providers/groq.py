import os
from groq import Groq

class GroqProvider:
    def __init__(self, config):
        self.config = config
        self.api_key = config['groq']['api_key']
        self.model = config['groq']['model']
        os.environ["GROQ_API_KEY"] = self.api_key
        self.client = Groq()

    def evaluate(self, post_content):
        prompt = f"""Rate the following Reddit post on a scale of 1 to 10, where 1 is very negative and 10 is very positive. Respond with only the numeric rating:

        {post_content}

        Rating:"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that rates Reddit posts based on their sentiment."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=5
        )

        rating_text = response.choices[0].message.content.strip()
        try:
            rating = int(rating_text)
            return max(1, min(10, rating))  # Ensure rating is between 1 and 10
        except ValueError:
            return 5  # Default to neutral if parsing fails