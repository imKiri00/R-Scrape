import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:1234@reddit-db/redit')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def create_tables():
    from .models import Base
    Base.metadata.create_all(engine)