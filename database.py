from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv


load_dotenv()



post_URL = os.getenv("URL")

URL = "sqlite:////home/sisir/Vscode-Python/Document/document.db"


Engine = create_engine(url=URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=Engine)

Base = declarative_base()



def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


