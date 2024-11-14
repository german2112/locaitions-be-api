from app.models.Event import EventSchema

class EventFactory:
    def create_event(event):
        return EventSchema(
            id=str(event["_id"]),
            name=event["name"],
            location=event["location"],
            rating=event["rating"],
            createdDate=event["createdDate"],
            status=event["status"],
            type=event["type"],
            description=event["description"],
            userId=event["userId"],
            clubId=event["clubId"],
            startDate=event["startDate"],
            endDate=event["endDate"],
            photos=event["photos"],
            capacity=event["capacity"],
            chatroomId=event["chatroomId"],
            isPrivate=event["isPrivate"],
            tags=event["eventTags"])