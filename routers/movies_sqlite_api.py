from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session
from modelos.models import MovieCreate, MovieResponse
from sqldb.db_session import get_db
from sqldb.movies_repo import MoviesRepository
from modelos.models import ErrorResponse
from modelos.models import SQLMovieListResponse
from modelos.models import DeleteMovieResponse

router2 = APIRouter(tags=["MoviesSQLite"])

def get_movies_repository(db: Session= Depends(get_db))-> MoviesRepository:
    return MoviesRepository(db)
    

@router2.post("/moviessqlite/",response_model=MovieResponse, responses={404: {"model": ErrorResponse},400:{"model":ErrorResponse}})
def create_movie_sqlite(movie_data: MovieCreate,repo : MoviesRepository = Depends(get_movies_repository)):
    """Endpoint to create a new movie in SQLite database"""
    movie = movie_data.model_dump()
    repo.create_movie(movie_data)
    if not movie:
        raise HTTPException(status_code=400, detail="Failed to create movie")
    return  {
        "success":True,
        "message": "movie created successfully",
        "data":movie
        }

@router2.get("/moviessqlite/",response_model=SQLMovieListResponse,responses={404: {"model": ErrorResponse},400:{"model":ErrorResponse}})
def get_all_movies_sqlite(repo: MoviesRepository = Depends(get_movies_repository)):
    """Endpoint to get all movies from SQLite database"""
    movies = repo.get_all_movies()
    if movies is None or len(movies) ==0:
        raise HTTPException(status_code=404, detail="No movies found in the database")
    return {
        "success":True,
        "message": f"{len(movies)} movies retrieved successfully",
        "data":movies,
        "total": len(movies)
        }
    
@router2.delete("/moviessqlite/{movie_id}", response_model=DeleteMovieResponse, responses={404: {"model": ErrorResponse}})
def delete_movie_sqlite(movie_id:int, repo: MoviesRepository = Depends(get_movies_repository)):
    """Endpoint to delete a movie from SQLlite database by ID"""
    movie = repo.delete_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail=f"Movie with ID {movie_id} not found")
    return {
        "success":True,
        "message": f"Movie with ID {movie_id} deleted successfully",
        "data":movie
        }
     
