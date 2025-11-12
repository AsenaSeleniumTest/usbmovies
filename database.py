#!usr/bin/env python3
import os
import json
from pathlib import Path
from typing import Dict, List, Optional


#Step 23 Define default database file path
# Step 25 
os.chdir("../movie-catalog-api")
DEFAULT_DB_FILE = Path("movies.json")

# Define a safe method to get the database file path
# I changed the way to define the path the function .with_name(filename) was givin me an error
DB_PATH: Path =  Path.cwd() / DEFAULT_DB_FILE

def get_db_path() -> Path:
    """Returns the path to the database file"""
    return DB_PATH

# Step 24 Ensure database file exists
def ensure_db_file_exists()-> Path:
    """Make sure the file database exists, create if not"""
    path = get_db_path()
    if not path.exists():
        path.parent.mkdir(parents = True, exist_ok = True)
        path.touch(exist_ok = True)
        #Step 27 
        path.write_text(json.dumps({"movies": [], "next_id":1},ensure_ascii = False, indent = 2),encoding="utf-8")
    return path

#Define class movidatabase 
class MovieDatabase:
    #Step 25
    #step 27 Adding Optional Path to __init__
    """Class to handle database movies catalog in memory"""
    def __init__(self, file_path: Optional[str] = None):
        #internal dictionary to store movies
        self.movies:dict[int,dict] = {}
        self.next_id: int = 1 # id for each new movie added will be incremented
        
        # Ruta del archivo 
        self._file_path: Path = Path(file_path) if file_path else get_db_path()
        ensure_db_file_exists()
        self.load_data()
    
    # Step 27 Data Consistency
    def load_data(self) -> None:
        """Read json database and movies
            If file empty or corrupt re-initialize
        """
        try:
            text = self._file_path.read_text(encoding="utf-8").strip()
            if not text:
                self.movies = {}
                self.next_id = 1
                self.save_data()
                return
            
            data =json.loads(text)
            
            #Step 27 data structure validation
            movies_list: List[Dict] = data.get("movies",[])
            next_id_val: int = data.get("next_id",1)
            
            # Load in memory as dict
            self.movies = {}
            for item in movies_list:
                #find id
                movie_id = item.get("id")
                if isinstance(movie_id, int):
                    self.movies[movie_id] = item
                    
            # if next id empty
            if isinstance(next_id_val, int) and next_id_val > 0:
                self.next_id = next_id_val
            else:
                self.next_id = (max(self.movies.keys())+1) if self.movies else 1
        except Exception as e:
            # if something goes wrong restart
            print(f"[MovieDatabase.load_data] error loading datos: {e}")
            self.movies={}
            self.next_id = 1
            self.save_data()
    
    
    def save_data(self)->None:
        """Dumps disk status to JSON format
            Format:
        {
          "movies": [ {...}, {...} ],
          "next_id": <int>
        }
        """    
        try:
            data = {
                "movies":list(self.movies.values()),
                "next_id": self.next_id
            }
            self._file_path.write_text(
                json.dumps(data, ensure_ascii = False, indent = 2),
                encoding="utf-8"
            )
        except Exception as e:
            print(f"[MovieDatabase.save_data] Error saving data: {e}")
            
                
            
    #step 27 Updated to memory operations     
    def add_movie(self,movie_data: dict) -> dict:
        """adds new movie to catalog, in memory, does not save in database yet"""
        movie_id = self.next_id
        #step 27
        record = {"id":movie_id, **movie_data}
        self.movies[movie_id] = record
        self.next_id += 1
        
        # Step 27 
        self.save_data()
        return record
    
    #This method searches for a matching text in the title of the movies
    def search_movies(self, query: str) -> List[dict]:
        """searches movies by text contained in the title"""
        query_lower = query.lower()
        movie_list= []
        for movie in self.movies.values():
            title_list = movie.get("title","").lower().split()
            if query_lower in title_list:
                movie_list.append(movie)
        return movie_list
    
    
    def  list_movies(self) -> list[dict]:
        """returns all movies in memory"""
        return list(self.movies.values())
    
    def get_movie(self,movie_id: int) -> Optional[dict]:
        """Returns a movie by id if found else None"""
        return self.movies.get(movie_id)
    
    def get_movie_by_year(self, year:int)-> List[dict]:
        """Returns a list of movies released in a given year"""
        return [movie for movie in self.movies.values() if movie.get("year") == year]
    
    def get_movie_by_director(self,director:str) -> List[dict]:
        """Returns a list of movies by a given director"""
        return [movie for movie in self.movies.values() if movie.get("director","").lower() == director.lower()]

    def get_movies_by_genre(self, genre:str)-> List[dict]:
        """Returns a list of movies by a given genre"""
        return [movie for movie in self.movies.values() if movie.get("genre","").lower() == genre.lower()]
    
if __name__ == "__main__":
    p2 = ensure_db_file_exists()
    print(f"Database file is located at: {p2}")
    print(f"Database file exists: {p2.exists()}")
    # Step 26 Test the Class 
    db1 = MovieDatabase()
    """db1.add_movie({"title":"Esspresso Polar","director":"Robin Williams","year":2009})
    db1.add_movie({"title":"Grown Ups","director":"Adam Sandler","year":2018})
"""    """print(db1.list_movies())
    print(db1.get_movie(2))
    print(db1.get_movie_by_year(2010))"""
    print(db1.get_movies_by_genre("drama"))
    