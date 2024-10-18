from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

app = FastAPI()

SQLALCHEMY_DATABASE_URL="postgresql://postgres:1234321@host:port/chat_message"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
Session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

