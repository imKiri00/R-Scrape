from dataclasses import dataclass
from datetime import datetime

@dataclass
class RedditPost:
    id: int
    headline: str
    content: str
    url: str
    created_at: datetime
    rating: float = None
    llm_evaluation: dict = None