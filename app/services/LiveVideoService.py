from app.models.User import UserSchema
from app.models.Event import EventSchema
from app.repositories import LiveVideoRepository
from bson.objectid import ObjectId

def validate_if_user_in_area(user: UserSchema, event: EventSchema):
    userCoordinates = (user.location["lng"], user.location["lat"])
    coordinatesThatIntersectsWithUser = list(LiveVideoRepository.validate_if_user_in_area(userCoordinates, ObjectId(event.uid)))
    return "False" if len(coordinatesThatIntersectsWithUser) == 0 else "True"