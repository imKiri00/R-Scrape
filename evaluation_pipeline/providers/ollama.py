import requests

class OllamaProvider:
    def __init__(self, config):
        self.config = config
        self.endpoint = config['ollama']['endpoint']
        self.model = config['ollama']['model']

    def evaluate(self, post_content):
        prompt = f"Rate the following Reddit post on a scale of 1 to 10, where 1 is very negative and 10 is very positive:\n\n{post_content}\n\nRating:"
        
        response = requests.post(
            f"{self.endpoint}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "max_tokens": 5
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            rating_text = result['response'].strip()
            try:
                rating = int(rating_text)
                return max(1, min(10, rating))  # Ensure rating is between 1 and 10
            except ValueError:
                return 5  # Default to neutral if parsing fails
        else:
            print(f"Error calling Ollama API: {response.status_code}")
            return 5  # Default to neutral on error