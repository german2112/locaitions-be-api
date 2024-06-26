from app.config import database
from app.models.JoinEventRequest import JoinEventRequest, JoinEventRequestStatus
from app.utils import TypeUtilities as typeUtilities
from bson import ObjectId


def insert(payload: JoinEventRequest):
    join_event_request = {
        **payload.dict(),
        "status": payload.status.value
    }
    return database.db["JoinEventRequests"].insert_one(join_event_request)


def update(id: str, payload: JoinEventRequest):
    join_event_request = {
        **payload.dict(),
        "status": payload.status.value
    }

    if "status" not in join_event_request:
        join_event_request["$or"] = [
            {
                "status": JoinEventRequestStatus.accepted.value
            },
            {
                "status": JoinEventRequestStatus.sent.value
            }
        ]

    return database.db["JoinEventRequests"].update_one({"_id": ObjectId(id)}, {"$set": {**join_event_request}})


def find(filters):

    return database.db["JoinEventRequests"].aggregate([
        {
            "$match": filters,
        },
        {
            "$lookup": {
                "from": "Users",
                "localField": "user_uid",
                "foreignField": "uid",
                "as": "user"
            }
        },
        {
            "$unwind": {
                "path": "$user",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$project": {
                "event_id": 1,
                "user_uid": 1,
                "status": 1,
                "last_updated": 1,
                "user.name": 1,
                "user.email": 1,
                "user.userName": 1,
                "user.profilePicture": 1
            }
        }
    ])
