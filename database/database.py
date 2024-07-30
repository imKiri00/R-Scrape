from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class RedditPostDB(Base):
    __tablename__ = 'reddit_posts'

    id = Column(Integer, primary_key=True)
    headline = Column(String)
    content = Column(Text)
    url = Column(String)
    created_at = Column(DateTime)
    rating = Column(Float)
    llm_evaluation = Column(JSON)

engine = create_engine('postgresql://postgres:1234@localhost/redit')
Session = sessionmaker(bind=engine)