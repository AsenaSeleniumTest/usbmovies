from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mongodb_models import Base

#Define session databases

engine = create_engine("sqlite:///./movies.db", echo=True, future=True)
Base.metadata.create_all(bind=engine)
async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency to get DB session"""
    db = async_session()
    try:
        yield db
    finally:
        db.close()
        