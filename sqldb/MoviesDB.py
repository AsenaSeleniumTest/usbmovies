
from sqlalchemy.orm import Session
from modelos.models import MovieCreate
from modelos.sqlitedb_models import Movie


    
class MoviesDB:
    """class to handle the movie catalof using SQLlite database with SQLAlchemy"""
    def __init__(self, db_manager: Session):
        self.db_manager = db_manager
        
    def add_movie(self, movie_data: MovieCreate) -> Movie:
        """Create a new movie entry in the database"""
        with self.db_manager.session_scope() as session:
            movie = Movie(title=movie_data.title,
                          director=movie_data.director,
                          year=movie_data.year,
                          genre=movie_data.genre,
                          duration=movie_data.duration,
                          rating=movie_data.rating,
                          synopsis=movie_data.synopsis,
                          price=movie_data.price,
                          is_watched=movie_data.is_watched)
            session.add(movie)
            session.commit()
            session.flush()  # To get the generated ID
            session.refresh(movie)
            return movie
    
    def get_movie_by_id(self, movie_id:int)-> Movie | None:
        """Retrieve a movie by its ID"""
        movie = self.db_manager.query(Movie).filter(Movie.id == movie_id).first()
        return movie