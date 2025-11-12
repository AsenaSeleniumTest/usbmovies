from sqlalchemy import create_engine,select
from sqlalchemy.orm import sessionmaker,Session
from mongodb_models import Movie,Base

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
        
class MovieSQLiteDB:
    """class to handle movie catalog using SQLAlchemy and SQLite""" 
    def __init__(self):
        self.db_session: Session = get_db()
        
    def get_movie_catalog(self) -> list[dict]:
        """Retrieve all movies from the database"""
        movies = select(Movie)
        return list(self.db_session.scalars(movies))