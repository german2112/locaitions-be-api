from app.config import database

def find_all():
    return database.db["MusicGenres"].find()

def insert_music_genre(musicGenre):
    return database.db["MusicGenres"].insert_one(musicGenre)