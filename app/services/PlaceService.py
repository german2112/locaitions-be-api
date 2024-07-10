from app.repositories import PlaceRepository as placeRepository
from app.models.User import UserSchema
from app.models.Place import PlaceSchema
from app.models.Photo import PhotoSchema
from app.factories.PlaceFactory import PlaceFactory
from app.schemas.PlaceFilter import PlaceFilter
from bson.objectid import ObjectId
from app.factories.EventFactory import EventFactory
from app.exceptions.NotFoundError import NotFoundError
from app.repositories import EventRepository
from app.exceptions.InternalServerError import InternalServerError

from geopy.distance import great_circle as GRC


def filter_list_of_places(user: UserSchema, placeAttributesToFilter: PlaceFilter):
    placeFilters = build_places_filters(placeAttributesToFilter)
    try:
        placesList = placeRepository.filter_places(placeFilters)
        formattedPlaces = format_places_list(
            user, placesList, placeAttributesToFilter.minimumDistance)
        return formattedPlaces
    except Exception as e:
        raise InternalServerError(e)

def build_places_filters(placeAttributesToFilter):
    placeFilters = {}
    if placeAttributesToFilter.name != "":
        placeFilters.update(
            {"name": {'$regex': placeAttributesToFilter.name, '$options': 'i'}})

    if placeAttributesToFilter.category != "":
        placeFilters.update({"category": placeAttributesToFilter.category})

    return placeFilters

def get_place_by_id(id: str):
    placeResult = {}
    try:
        foundPlace = placeRepository.get_by_id(ObjectId(id))
        if foundPlace != None:
            placeResult = PlaceFactory.create_place(foundPlace).to_dict()
        return placeResult
    except Exception as e:
        raise InternalServerError(e)

def calculate_user_to_place_distance(userCoordinates, placeCoordinates):
    if userCoordinates == None:
        return "User Coordinates cannot be empty."

    if placeCoordinates == None:
        return "Place Coordinates cannot be empty."

    return round(GRC(userCoordinates, placeCoordinates).km, 2)


def format_places_list(user: UserSchema, placesList, minimumDistanceFilter: float):
    formattedPlaces = []
    for place in placesList:
        validatedDistanceBetweenPlaceAndUser = validate_if_place_inside_user_range(
            user, minimumDistanceFilter, place["location"]["mainCoordinates"]["coordinates"])
        if 1 == 1:
            placeItem = PlaceFactory.create_place(place).to_dict()
            formattedPlaces.append(placeItem)
    return formattedPlaces

def validate_if_place_inside_user_range(user: UserSchema, minimumDistanceFilter, place):
    userCoordinates = (user.location["lat"], user.location["lng"])
    minimumDistance = minimumDistanceFilter if minimumDistanceFilter != None else 20
    placeOutOfUserRange = -1
    placeCoordinates = (place[1], place[0])
    distanceBetweenUserAndPlace = calculate_user_to_place_distance(
        userCoordinates, placeCoordinates)
    if distanceBetweenUserAndPlace <= minimumDistance:
        return distanceBetweenUserAndPlace
    return placeOutOfUserRange

def get_place_event(placeId: str, longitude: float, lattitude: float, status: str):
    try:
        foundPlaceEventCursor = EventRepository.get_place_event(placeId, longitude, lattitude, status)
        if not foundPlaceEventCursor._has_next():
            raise NotFoundError("No Active event found for the given place")
        placeEvent = foundPlaceEventCursor.next()
        return EventFactory.create_event(placeEvent).to_dict()
    except Exception as e:
        raise InternalServerError(e)
