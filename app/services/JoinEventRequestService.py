from app.models.JoinEventRequest import JoinEventRequest
from app.repositories import JoinEventRequestRepository as joinEventRequestRepository
from app.exceptions.InternalServerError import InternalServerError
from app.utils.TypeUtilities import parse_json
from bson import ObjectId


def insert(payload: JoinEventRequest):
    try:
        inserted_id = joinEventRequestRepository.insert(payload).inserted_id
        return str(inserted_id)
    except Exception as e:
        raise InternalServerError(
            f"Error while inserting a join event request Error: {str(e)}")


def update(id: str, payload: JoinEventRequest):
    try:
        joinEventRequestRepository.update(id, payload)
        updated_request = joinEventRequestRepository.find(
            {"_id": ObjectId(id)})
        return _format_join_event_requests(updated_request)
    except Exception as e:
        raise InternalServerError(
            f"Error while inserting a join event request Error: {str(e)}")


def find(event_id: str, user_uid: str, status: str):
    try:
        filters = {}
        if (event_id != None):
            filters["event_id"] = event_id

        if (user_uid != None):
            filters["user_uid"] = user_uid

        if (status != None):
            filters["status"] = status

        join_event_requests = joinEventRequestRepository.find(filters)
        
        return _format_join_event_requests(join_event_requests)
    except Exception as e:
        raise InternalServerError(
            f"Error while inserting a join event request Error: {str(e)}")


def _format_join_event_requests(requests):
    formatted_requests = []
    for request in requests:
        formatted_requests.append({
            **parse_json(request),
            "_id": str(request["_id"]),
            "last_updated": str(request["last_updated"]) if request is not None else None
        })

    return formatted_requests
