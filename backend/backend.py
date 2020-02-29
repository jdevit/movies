from api.imdbAPI import ImdbAPI
from database.database import Database

#TODO: Rethink if backend.py is necessary.

# Frontend + Interface calls backend methods
# Backend links with: API, Database, Analysis

class Backend:

    @staticmethod
    def process_url(url):
        imdb_api = ImdbAPI(url)
        film = imdb_api.get_movie_details()

        # Save movie details to db

