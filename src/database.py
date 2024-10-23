from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL="postgresql://postgres:1234321@localhost:5432/chat_message"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
Session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = Session_local()
    try:
        yield db
    finally:
        db.close()

