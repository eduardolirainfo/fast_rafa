from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fast_rafa.core.settings import Settings

engine = create_engine(Settings().DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
