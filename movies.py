from fastapi import APIRouter, HTTPException
from database import MovieDatabase
from models import MovieCreate
from models import MovieUpdate
from models import MovieResponse
from models import MovieListResponse
from models import ErrorResponse


#Step 30 Add GET endpoint to list movies
#Creating router instance
router = APIRouter(tags=["Movies"])
#Creating database instance
db = MovieDatabase()


#Step 39 Add endpoint to create a new movie
@router.post("/movies",status_code = 201, response_model= MovieResponse)
def create_movie(movie: MovieCreate):
    """Endpoint to create a new movie entry and store it in the database"""
    #Validation required fields
    data = movie.model_dump()
    
    created = db.add_movie(data)
    db.save_data()

    return {
        "success":True,
        "message": "movie created successfully",
        "data":created
    }

    
#Adding endpoint to get list of movies by year with Path Parameter
@router.get("/movies/{year}", response_model= MovieListResponse)
async def get_movies_by_year(year: int):
    """End point to get movies by release year"""
    movies =db.get_movie_by_year(year)
    if movies is None or len(movies) ==0:
        raise HTTPException(status_code=404, detail=f"No movies found for year {year}")
    return {
        "success":True,
        "message":f"{len(movies)} movies found for year {year}",
        "data":movies,
        "total": len(movies)
    }
##Adding endpoint to get the list of movies by director Path  parameter
@router.get("/movies/director/{director}", response_model= MovieListResponse, responses={404: {"model": ErrorResponse}})
async def get_movies_by_director(director: str):
    """Get the movies based on director name"""
    movies_director = db.get_movie_by_director(director)
    if movies_director is None or len(movies_director) ==0:
        raise HTTPException(status_code=404, detail=f"No movies found for director {director}")
    return{
        "success":True,
        "message":f"{len(movies_director)}movies matching director {director}",
        "data": movies_director,
        "total":len(movies_director)
    }
    
#return movies by Genre path parameter
@router.get("/movies/genre/{genre}", response_model= MovieListResponse, responses={404: {"model": ErrorResponse}})
async def get_movies_by_genre(genre: str):
    """Get the movies base on genre""" 
    movies_genre = db.get_movies_by_genre(genre)
    if movies_genre is None or len(movies_genre) ==0:
        raise HTTPException(status_code=404, detail=f"No movies found for genre {genre}")
    return{
        "success":True,
        "message":f"{len(movies_genre)} movies matching genre {genre}",
        "data": movies_genre,
        "total":len(movies_genre)
    }
    
@router.get("/movies/search/{text_query}", response_model= MovieListResponse, responses={404: {"model": ErrorResponse}})
async def search_in_movies_title(text_query: str):
    """Endpoint to search movies by text in title"""
    search_results = db.search_movies(text_query)
    if search_results is None or len(search_results) ==0:
        raise HTTPException(status_code=404, detail=f"No movies found matching search query : {text_query}")
    return {
        "success":True,
        "message":f"{len(search_results)} movies found matching search query : {text_query}",
        "data":search_results,
        "total": len(search_results)
    }
    
    
#Step 47 udpdate Get endpoint to list movies to use MovieListResponse model
@router.get("/movies",response_model = MovieListResponse)
def list_movies():
    """Endpoint to list all movies"""
    items = db.list_movies()
    return {
        "success":True,
        "message":f"{len(items)} movies found",
        "data":items,
        "total": len(items)
    }


#Step  33
@router.get("/movies/{movie_id}", response_model = MovieResponse,responses = {404: {"model": ErrorResponse},400:{"model":ErrorResponse}})
def get_movie(movie_id: int):
    """Endpoint to get a movie by its ID"""
    movie = db.get_movie(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail=f"Movie not found with id : {movie_id}")
    return movie

# step 35 Put endpoint to update movie details
#Step 43 Refacto Update to use Pydantic models class
@router.put("/movies/{movie_id}", response_model= MovieResponse, responses={404: {"model": ErrorResponse},400:{"model":ErrorResponse}})
def update_movie(movie_id: int, movie_data: MovieUpdate):
    """Endpoint to update existing movie details"""
    movie = db.get_movie(movie_id)
    if movie is None:
        raise HTTPException(status_code=404,detail=f"Movie not found with id : {movie_id}")
    
    #Update only provided fields
    update_data  = movie_data.model_dump(exclude_unset=True)
    
    movie.update(update_data)
    db.movies[movie_id] = movie
    db.save_data()
    
    return {
        "success":True,
        "message":f"Movie with id {movie_id} updated successfully",
        "data":movie
    }
    
#Step 37 Delete endpoint to remove a movie    
@router.delete("/movies/{movie_id}", response_model= MovieResponse, responses={404: {"model": ErrorResponse},400:{"model":ErrorResponse}})
def delete_movie(movie_id:int):
    """Endpoint to delete a movie by its ID"""
    movie = db.get_movie(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail=f"Movie not found with id : {movie_id}")
    
    #Delete the movie
    del db.movies[movie_id]
    db.save_data()
    
    return {
        "success":True,
        "message":f"Movie with id {movie_id} deleted successfully"
    }