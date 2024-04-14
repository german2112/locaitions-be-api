from app.models.EventFilters import EventFiltersSchema
from app.repositories import EventRepository
from bson.objectid import ObjectId

def get_events_by_filter(event: EventFiltersSchema):
    filters = build_event_filters(event)
    print(filters)
    return EventRepository.filter_events(filters)

def build_event_filters(event: EventFiltersSchema):
    eventFilters = {}

    if(event.name):
        eventFilters["name"] = event.name
    if(event.date):
        eventFilters["date"] = event.date
    if(event.clubId):
        eventFilters["clubId"] = ObjectId(event.clubId)
    if(event.type):
        eventFilters["type"] = event.type
    if(event.userId):
        eventFilters["userId"] = event.userId
    if(event.location):
        eventFilters["location"] = event.location
    if(event.status):
        eventFilters["status"] = event.status
    
    return eventFilters