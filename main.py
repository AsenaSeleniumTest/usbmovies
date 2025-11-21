from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from config import settings
from modelos.models import MovieCreate
from modelos.models import ErrorResponse
from modelos.sqlitedb_models import Base
from routers import movies_sqlite_api
from routers import movies
from sqldb.db_session import engine


#creating instance of FastAPI
#Step 13 adding settings to FastAPI instance
#Step 20 Add POST endpoint in main.py
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Movie Catalog API", version="1.0.0", description="API for managing a basic movie catalog", debug=settings.debug)

#defininf main endpoint
#Step 13 updating the name frome read_root to root and use async function
@app.get("/")
async def root():
    """Root endpoint returning a welcome message"""
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
        content = ErrorResponse(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc),error_type="Could not process data").model_dump()
        
    )

app.include_router(movies_sqlite_api.router2, prefix="/apilite/v1")
app.include_router(movies.router, prefix="/api/v1")
