from typing import List, Optional
from sqlalchemy.orm import Session
from .models import RedditPost

class RedditPostDB:
    def __init__(self, id, headline, content, url, created_at, rating=None, llm_evaluation=None):
        self.id = id
        self.headline = headline
        self.content = content
        self.url = url
        self.created_at = created_at
        self.rating = rating
        self.llm_evaluation = llm_evaluation

class RedditPostRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, post: RedditPost) -> RedditPost:
        db_post = RedditPostDB(
            headline=post.headline,
            content=post.content,
            url=post.url,
            created_at=post.created_at
        )
        self.session.add(db_post)
        self.session.commit()
        self.session.refresh(db_post)
        post.id = db_post.id
        return post

    def get_by_id(self, post_id: int) -> Optional[RedditPost]:
        db_post = self.session.query(RedditPostDB).filter(RedditPostDB.id == post_id).first()
        if db_post:
            return RedditPost(
                id=db_post.id,
                headline=db_post.headline,
                content=db_post.content,
                url=db_post.url,
                created_at=db_post.created_at,
                rating=db_post.rating,
                llm_evaluation=db_post.llm_evaluation
            )
        return None

    def get_all(self) -> List[RedditPost]:
        db_posts = self.session.query(RedditPostDB).all()
        return [
            RedditPost(
                id=post.id,
                headline=post.headline,
                content=post.content,
                url=post.url,
                created_at=post.created_at,
                rating=post.rating,
                llm_evaluation=post.llm_evaluation
            ) for post in db_posts
        ]

    def update(self, post: RedditPost) -> RedditPost:
        db_post = self.session.query(RedditPostDB).filter(RedditPostDB.id == post.id).first()
        if db_post:
            db_post.headline = post.headline
            db_post.content = post.content
            db_post.url = post.url
            db_post.created_at = post.created_at
            db_post.rating = post.rating
            db_post.llm_evaluation = post.llm_evaluation
            self.session.commit()
            self.session.refresh(db_post)
            return post
        raise ValueError(f"No post found with id {post.id}")

    def delete(self, post_id: int) -> bool:
        db_post = self.session.query(RedditPostDB).filter(RedditPostDB.id == post_id).first()
        if db_post:
            self.session.delete(db_post)
            self.session.commit()
            return True
        return False

    def get_unrated_posts(self) -> List[RedditPost]:
        db_posts = self.session.query(RedditPostDB).filter(RedditPostDB.rating == None).all()
        return [
            RedditPost(
                id=post.id,
                headline=post.headline,
                content=post.content,
                url=post.url,
                created_at=post.created_at,
                rating=post.rating,
                llm_evaluation=post.llm_evaluation
            ) for post in db_posts
        ]