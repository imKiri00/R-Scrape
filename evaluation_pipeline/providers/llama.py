from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class LlamaProvider:
    """
    A provider class for evaluating posts using the Llama model.
    """

    def __init__(self, config):
        """
        Initialize the LlamaProvider with the given configuration.

        Args:
            config (dict): Configuration dictionary containing model details.
        """
        self.config = config
        self.model_name = config['llama']['model']
        # Load the pre-trained tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)

    def evaluate(self, post_content):
        """
        Evaluate the given post content using the Llama model.

        Args:
            post_content (str): The content of the post to be evaluated.

        Returns:
            int: A rating between 1 and 10 based on the post's sentiment.
        """
        # Tokenize the input text
        inputs = self.tokenizer(post_content, return_tensors="pt", truncation=True, max_length=512)
        
        # Perform inference without gradient computation
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # Extract the sentiment score (assuming the model outputs a score between 0 and 1)
        sentiment_score = torch.sigmoid(outputs.logits).item()
        
        # Convert sentiment score to a rating between 1 and 10
        rating = 1 + int(sentiment_score * 9)
        
        return rating