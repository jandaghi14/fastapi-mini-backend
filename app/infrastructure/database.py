
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL is None:
    DATABASE_URL = os.getenv('DATABASE_URL_TEST')

if DATABASE_URL is None:
    raise Exception("Database cannot be found")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
