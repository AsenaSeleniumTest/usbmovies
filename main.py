from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from config import settings
from models import MovieCreate
import movies
#creating instance of FastAPI
#Step 13 adding settings to FastAPI instance
# Step 20 Add POST endpoint in main.py
app = FastAPI(title="Movie Catalog API", version="1.0.0", description="API for managing a basic movie catalog", debug=settings.debug)

#defininf main endpoint
#Step 13 updating the name frome read_root to root and use async function
@app.get("/")
async def root():
    #This is the main endpoint that returns a welcome message
    return {"message": "Welcome to the USBMovie Catalog API!"}

# Step 20 
@app.post("/movies")
async def create_movie(payload: MovieCreate):
    """Endpoint to create a new movieentry  """
    return {
        "success":True,
        "message":"Movie Received not Stored yet",
        "data":payload.model_dump()
        }

#Adding exception handlers  ### Review getting server errors#####
@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    """Custom handler for HTTP exceptions"""
    return JSONResponse(
        status_code= exc.status_code,
        content = {
            "detail": exc.detail,
            "status_code": exc.status_code
        }
    )
    
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Custom handler for request validation errors"""
    return JSONResponse(
        status_code= status.HTTP_422_UNPROCESSABLE_ENTITY,
        content = {
            "detail": exc.errors(),
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY
        }
    )
    
@app.exception_handler(Exception)
def general_exception_handler(request: Request, exc: Exception):
    """Custom handler for general exceptions"""
    return JSONResponse(
        status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
        content = {
            "detail": str(exc),
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    )
    
app.include_router(movies.router, prefix="/api/v1")
