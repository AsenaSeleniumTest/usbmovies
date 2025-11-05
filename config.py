#!/usr/bin/env python3
from typing import List
from pydantic_settings import BaseSettings
from pydantic import ConfigDict



class Settings(BaseSettings):
    #Base Configuration of the application
    #general info
    app_name: str = "USB Movie Catalog API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    #server settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    #CORS settings
    cors_origins: List[str] = ["*"]
    
    # database file settings
    database_file: str = "movies.json"
    
    #Predefined path  
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    
    #pydantic configuration
    model_config = ConfigDict(case_sensitive=False,extra="ignore")
    
    
    #global settings instance

settings = Settings()


def get_config_summary()-> dict:
    """Returns a simple config local summary""" 
    return {
        "app_name":settings.app_name,
        "app_version":settings.app_version,
        "debug":settings.debug
    }   