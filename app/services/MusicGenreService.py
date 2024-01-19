from app.repositories import MusicGenreRepository
from app.models import MusicGenre
from fastapi.encoders import jsonable_encoder

def get_music_genre_list():
    response = list()
    musicGenreList = MusicGenreRepository.find_all()
    for musicGenre in musicGenreList:
        #TODO Convert cursor to MusicGenre entity and insert it to the list
        response.append({
            "id": str(musicGenre["_id"]),
            "name": musicGenre["name"]
        })
    return {"message": "Request processed successfully", "body": response}

def insert_music_genre(musicGenre: MusicGenre):
    #TODO fix response to deliver the object instead of only the id
    return MusicGenreRepository.insert_music_genre(jsonable_encoder(musicGenre)).inserted_id
    