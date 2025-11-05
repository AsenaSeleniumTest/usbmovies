#!/usr/bin/env python3
from datetime import date
from typing import Optional
from typing import List
from pydantic import BaseModel
from pydantic import field_validator
from pydantic import Field


#Step 15 creating Movie model
#step 16 complete the movie class definition
# Step 17 Update models with custom field descriptions and constraints
#Step 20 Add POST endpoint in main.py
# step 22 endpoint tested in the uvicorn server 
class MovieBase(BaseModel):
    """"Movie model representing a movie in the catalog
    """
    
    #Title of the movie
    title: str = Field(...,min_length=1, max_length=200, description = "Title of the movie")
    #The Director of the movie
    director: str = Field(..., min_length = 1, max_length = 100, description = "Director of the movie")
    #Release year of the movie
    year: int = Field(..., ge = 1880, le = 2030, description = "Release year of the movie")
    #Genre of the movie(horror,comedy,drama,action,romance,sci-fi,other)
    genre: str = Field(..., min_length = 1, max_length = 50, description = "Genre of the movie")
    #Duration of the movie in minutes
    duration: Optional[int] = Field(None, ge =1, le =300, description = "Duration of the movie in minutes")
    # General Rating of the movie
    rating: Optional[float] = Field(None, ge = 0.0, le = 10.0, description = "General rating of the movie")
    # Brief description or synopsis of the movie
    synopsis: Optional[str] = Field(None,max_length = 1000, description ="Synopsis of the movie")
    # price of the movie
    price : Optional[float] = Field(None, ge  =0.0, description = "Price of the movie")
    # movie already watched
    is_watched: bool = Field(default= False, description = "Indicates if the movie has been watched by the user")
    
    # Adding custom validations 
    #Step 18 
    @field_validator('year')
    @classmethod
    def validate_year(cls, value: int) -> int:
        """Validate year to be in range"""
        if value < 1880:
            raise ValueError("Year must be greater than or equal to 1880")
        if value > date.today().year + 5:
            raise ValueError("Year cannot be in the far future")
        return value
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, value : str)-> str:
        """Validate the title is not empty or whitespaces"""
        if not value.strip():
            raise ValueError("Title cannot be empty or whitespace made")
        return value.strip()
    

#model for updating a movie 
class MovieUpdate(BaseModel):
    """Model Base for updating a movie entry"""
    title: Optional[str] = Field(None, min_length = 1, max_length=200)
    director: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=1880, le=2030)
    genre: Optional[str] = Field(None, min_length=1, max_length=50)
    duration: Optional[int] = Field(None, ge=1, le=300)
    rating: Optional[float] = Field(None, ge=0.0, le=10.0)
    synopsis: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, ge=0.0)
    is_watched: Optional[bool] = None

class MovieResponse(BaseModel):
    """Class model for responses from the API"""
    success: bool = Field(..., description = "States if  the API call was successful")
    message: str = Field(..., description  = "Message to the client")
    data: Optional[dict] = Field(None, description = "Returned movie or None if not applicable")
    
class MovieListResponse(BaseModel):
    """Class for response when listing multiple movies"""
    success: bool = Field(..., description = "States if  the API call was successful")
    message: str = Field(..., description  = "Message to the client")
    data: List[dict] = Field(default_factory= list, description = "List of returned movies or None if not applicable")
    total: int = Field(..., description = "Total number of movies returned")
    
class ErrorResponse(BaseModel):
    """Class model for error responses from the API """  
    status_code: int = Field(..., description = "HTTP status code of the error")
    detail: str = Field(..., description="Detailed error message")
    error_type: Optional[str] = Field(None, description = "Type of error")
    

class MovieCreate(MovieBase):
    """Model Base for creating a new movie entry"""
    pass



#step 19 test the validators for year and title
if __name__ == "__main__":
    movie = MovieCreate(
    title="Inception",
    director="Christopher Nolan",
    year=2031,
    genre="Sci-Fi"
    )
    print(movie.model_dump())