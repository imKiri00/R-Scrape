from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import RedditPost

class RedditPostRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, post: RedditPost):
        self.session.add(post)

    async def commit(self):
        await self.session.commit()

    async def refresh(self, post: RedditPost):
        await self.session.refresh(post)

    async def get_by_id(self, post_id: int):
        result = await self.session.execute(select(RedditPost).filter(RedditPost.id == post_id))
        return result.scalar_one_or_none()
