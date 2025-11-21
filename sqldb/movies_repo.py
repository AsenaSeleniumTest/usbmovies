from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List, Optional
from modelos.models import MovieCreate
from modelos.sqlitedb_models import Movie as MovieModel


class MoviesRepository:
    """Class to handle movie operations for the database CRUD operations"""
    def __init__(self, db: Session):
        self.db = db
        
    def create_movie(self, movie_data: MovieCreate) -> MovieModel:
        """Create a new movie entry in the database"""
        try:
            movie = MovieModel(title = movie_data.title,
                              director = movie_data.director,
                              year = movie_data.year,
                              genre = movie_data.genre,
                              duration = movie_data.duration,
                              rating = movie_data.rating,
                              synopsis = movie_data.synopsis,
                              price = movie_data.price,
                              is_watched = movie_data.is_watched
                              )
            self.db.add(movie)
            self.db.commit()
            self.db.refresh(movie)
            return movie
        except IntegrityError as e:
            self.db.rollback()
    
    def get_movie_by_id(self, movie_id: int)->MovieModel:
        movie = self.db.query(MovieModel).filter(MovieModel.id == movie_id).first()
        return movie
    
    def get_movie_by_year(self, year:int)-> List[MovieModel]:
        movies = self.db.query(MovieModel).filter(MovieModel.year == year).all()
        return movies
    
    def get_all_movies(self) -> List[str]:
        movies = self.db.query(MovieModel).all()
        if movies is None or len(movies) ==0:
            return ["No movies found in the database",]
        return list(str(movies))
            