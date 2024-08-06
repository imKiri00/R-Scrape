from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RedditPost(Base):
    __tablename__ = 'reddit_posts'

    id = Column(Integer, primary_key=True)
    headline = Column(String)
    content = Column(Text)
    url = Column(String)
    created_at = Column(DateTime)
    rating = Column(Float)
    llm_evaluation = Column(JSON)