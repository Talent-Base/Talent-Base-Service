import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///:memory:')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def getDatabase(expire_on_commit: bool = True):
	db = SessionLocal(expire_on_commit=expire_on_commit)
	try:
		yield db
	finally:
		db.close()
