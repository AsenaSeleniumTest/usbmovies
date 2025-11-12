from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from config import settings
from models import MovieCreate
from models import ErrorResponse
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
    """Endpoint to create a new movie entry  """
    return {
        "success":True,
        "message":"Movie Received not Stored yet",
        "data":payload.model_dump()
        }



#Adding exception handlers  ### Review getting server errors#####
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Custom handler for request validation errors"""
    return JSONResponse(
        status_code= status.HTTP_422_UNPROCESSABLE_ENTITY,
        content =  ErrorResponse(details=str(exc.errors()), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, error_type="Validation Error").model_dump()
        
    )
#Adding exception handlers  ### Review getting server errors#####
@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    """Custom handler for HTTP exceptions"""
    return JSONResponse(
        status_code= exc.status_code,
        content = ErrorResponse(status_code= exc.status_code, detail= exc.detail,error_type="Not Found Item").model_dump()
        
    )
    

    
@app.exception_handler(Exception)
def general_exception_handler(request: Request, exc: Exception):
    """Custom handler for general exceptions"""
    return JSONResponse(
        status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
        content = ErrorResponse(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)).model_dump()
        
    )
    
app.include_router(movies.router, prefix="/api/v1")
