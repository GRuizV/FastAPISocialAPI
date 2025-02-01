from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from decouple import config
from typing import Generator



# CONSTANTS SETTING
DB_USER = config('DB_USER')
DB_NAME = config('DB_NAME')
DB_PASS = config('DB_PASS')

SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@localhost/{DB_NAME}'


# SQLALCHEMY ORM SETTING
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()




# Database instance generator, later will be the dependency in the endpoint definition
def get_db() -> Generator[Session, None, None]:

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()





