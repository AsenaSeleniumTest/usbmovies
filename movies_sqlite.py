from fastapi import APIRouter, HTTPException,Depends
from sqldb.db_session import MovieSQLiteDB

@router.get("/moviessqlite/")
def get_all_movies():
    """Endpoint to get all movies from SQLite database"""
    db = MovieSQLiteDB()
    movies = db.get_movie_catalog()
    if movies is None:
        raise HTTPException(status_code=404, detail="No movies found in the database")
    