from app.repositories import PlaceRepository as placeRepository
from app.models.User import UserSchema
from app.models.Place import PlaceSchema
from app.dto.PlaceDTO import PlaceDTO
from app.entities.Photo import Photo
from bson.objectid import ObjectId

from geopy.distance import great_circle as GRC

def get_list_of_places(user: UserSchema, placeAttributesToFilter: PlaceSchema):

    placeFilters = build_places_filters(placeAttributesToFilter)
       
    placesList = placeRepository.get(placeFilters)
    formattedPlaces = format_places_list(user, placesList, placeAttributesToFilter)
    return formattedPlaces

def get_place_by_id(id: int):
    placeFilter = {"_id": ObjectId(id)}
    result = placeRepository.get(placeFilter)

    if result._has_next():
        foundPlace = result.next()
        placePhotos = build_photo_object_of_place(foundPlace)
        return PlaceDTO(
                    str(foundPlace["_id"]),
                    foundPlace["name"],
                    foundPlace["location"],
                    0,
                    placePhotos,
                    foundPlace['description']).to_dict()
    
    return "Place not found"

def build_places_filters(placeAttributesToFilter):
    placeFilters = {}
    if placeAttributesToFilter.name != None:
        placeFilters.update({"name": {'$regex':placeAttributesToFilter.name, '$options': 'i'}}) 

    if placeAttributesToFilter.category != None:
        placeFilters.update({"category": placeAttributesToFilter.category})

    return placeFilters

def calculate_user_to_place_distance(userCoordinates, placeCoordinates):
    if userCoordinates == None:
        return "User Coordinates cannot be empty."
    
    if placeCoordinates == None:
        return "Place Coordinates cannot be empty."
    
    return round(GRC(userCoordinates, placeCoordinates).km,2)
    
def format_places_list(user: UserSchema,placesList, placeAttributesToFilter: PlaceSchema):
    if placesList == None:
        return "List of places cannot be empty"
    
    formattedPlaces = []

    for place in placesList:
        validatedDistanceBetweenPlaceAndUser = validate_if_place_inside_user_range(user, placeAttributesToFilter, place["location"]["mainCoordinates"]["coordinates"])
        if validatedDistanceBetweenPlaceAndUser >= 0:
            
            photo = build_photo_object_of_place(place)
            
            placeResult = PlaceDTO(
                str(place["_id"]),
                place["name"],
                place["location"],
                str(validatedDistanceBetweenPlaceAndUser) + "km",
                photo,
                place["description"]
                )

            formattedPlaces.append(placeResult.to_dict())

    return formattedPlaces

def validate_if_place_inside_user_range(user: UserSchema, placeAttributesToFilter, place):
    userCoordinates = (user.location["lat"], user.location["lng"])
    
    minimumDistance = placeAttributesToFilter.minimumDistance if placeAttributesToFilter.minimumDistance != None else 20
    placeOutOfUserRange = -1
    placeCoordinates = (place[1], place[0])
    distanceBetweenUserAndPlace = calculate_user_to_place_distance(userCoordinates, placeCoordinates)
    if distanceBetweenUserAndPlace <= minimumDistance:
        return distanceBetweenUserAndPlace
    return placeOutOfUserRange

def build_photo_object_of_place(place):
    photo = []
    if len(place["placePhotos"]) != 0:
        photo = Photo(place["placePhotos"][0]["filename"],
                    place["placePhotos"][0]["fileUrl"],
                    place["placePhotos"][0]["createdAt"]
                    ).to_dict()
    return photo