from app.repositories import PlaceRepository as placeRepository
from app.models.User import UserSchema
from app.dto.PlaceDTO import PlaceDTO
from app.entities.Photo import Photo

import geopy.distance


def get_list_of_places(user: UserSchema):
    placesList = placeRepository.get()
    formattedPlaces = format_places_list(user, placesList)
    return formattedPlaces

def calculate_user_to_place_distance(userCoordinates, placeCoordinates):
    if userCoordinates == None:
        return "User Coordinates cannot be empty."
    
    if placeCoordinates == None:
        return "Place Coordinates cannot be empty."
    
    return round(geopy.distance.geodesic(userCoordinates, placeCoordinates).km,2)
    
def format_places_list(user: UserSchema,placesList):
    if placesList == None:
        return "List of places cannot be empty"
    
    userCoordinates = (user.location["lat"], user.location["lng"])
    formattedPlaces = []

    for place in placesList:
        photo = []
        if len(place["placePhotos"]) != 0:
            photo = Photo(place["placePhotos"][0]["filename"],
                        place["placePhotos"][0]["fileUrl"],
                        place["placePhotos"][0]["createdAt"]
                        ).to_dict()
        
        placeCoordinates = (place["location"]["lat"], place["location"]["lng"])
        distanceBetweenUserAndPlace = calculate_user_to_place_distance(userCoordinates, placeCoordinates)
        placeResult = PlaceDTO(
            place["name"],
            place["location"],
            place["address"],
            str(distanceBetweenUserAndPlace) + "km",
            photo)

        formattedPlaces.append(placeResult.to_dict())
    
    return formattedPlaces
    