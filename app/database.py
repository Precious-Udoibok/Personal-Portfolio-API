#connect your database to sqlalchemy

from sqlalchemy import create_engine #use to establist connection
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


#use relative file path
DB_URL = "sqlite:///./portfolio.db" #database credential

engine = create_engine(DB_URL, connect_args={'check_same_thread': False}) #connect to the database

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False) #interact with db

Base = declarative_base() #provide us with all the tools to create table in our database

#access the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()