from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from typing import Optional, Generator
from contextlib import contextmanager
from modelos.sqlitedb_models import Base

#Define session databases

#engine = create_engine("sqlite:///./movies.db", echo=True, future=True)
#Base.metadata.create_all(bind=engine)
#async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DATABASE_URL="sqlite:///./movies.db"

engine = create_engine(DATABASE_URL,
                       echo=True,
                       future=True,
                       connect_args={"check_same_thread": False}
                       )

#create the session local class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#dependency injection
def get_db() -> Generator[Session,None,None]:
    """Dependency to get the database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
            
