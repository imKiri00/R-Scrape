from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.dialects.postgresql import JSONB

DATABASE_URL = "postgresql+asyncpg://kiri:1234@localhost/reddit_scraper"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

class RedditPost(Base):
    __tablename__ = "reddit_posts"

    id = Column(Integer, primary_key=True, index=True)
    headline = Column(String(255))
    content = Column(Text)
    url = Column(String(255))
    created_at = Column(DateTime)
    rating = Column(Float)
    llm_evaluation = Column(JSONB)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session