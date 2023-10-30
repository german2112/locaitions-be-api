from app.repositories import PlaceRepository as placeRepository
from app.models.User import UserSchema
from app.models.Place import PlaceSchema
from app.dto.PlaceDTO import PlaceDTO
from app.entities.Photo import Photo

import geopy.distance

def get_list_of_places(user: UserSchema, placeAttributesToFilter: PlaceSchema):

    placeFilters = build_places_filters(placeAttributesToFilter)
       
    placesList = placeRepository.get(placeFilters)
    formattedPlaces = format_places_list(user, placesList, placeAttributesToFilter)
    return formattedPlaces

def build_places_filters(placeAttributesToFilter):
    placeFilters = {}
    if placeAttributesToFilter.name != None:
        placeFilters.update({"name": placeAttributesToFilter.name}) 

    if placeAttributesToFilter.category != None:
        placeFilters.update({"category": placeAttributesToFilter.category})

    return placeFilters

def calculate_user_to_place_distance(userCoordinates, placeCoordinates):
    if userCoordinates == None:
        return "User Coordinates cannot be empty."
    
    if placeCoordinates == None:
        return "Place Coordinates cannot be empty."
    
    return round(geopy.distance.geodesic(userCoordinates, placeCoordinates).km,2)
    
def format_places_list(user: UserSchema,placesList, placeAttributesToFilter: PlaceSchema):
    if placesList == None:
        return "List of places cannot be empty"
    
    userCoordinates = (user.location["lat"], user.location["lng"])
    formattedPlaces = []
    minimumDistance = placeAttributesToFilter.minimumDistance if placeAttributesToFilter.minimumDistance != None else 20

    for place in placesList:
        placeCoordinates = (place["location"]["lat"], place["location"]["lng"])
        distanceBetweenUserAndPlace = calculate_user_to_place_distance(userCoordinates, placeCoordinates)
        if distanceBetweenUserAndPlace <= minimumDistance:
            photo = []
            if len(place["placePhotos"]) != 0:
                photo = Photo(place["placePhotos"][0]["filename"],
                            place["placePhotos"][0]["fileUrl"],
                            place["placePhotos"][0]["createdAt"]
                            ).to_dict()
            
            placeResult = PlaceDTO(
                place["name"],
                place["location"],
                place["address"],
                str(distanceBetweenUserAndPlace) + "km",
                photo)

            formattedPlaces.append(placeResult.to_dict())
    
    
    return formattedPlaces
    