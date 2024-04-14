from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.models.EventFilters import EventFiltersSchema
from app.utils import TypeUtilities
from app.services import EventService as eventService

eventsRouter = APIRouter(prefix="/events")

@eventsRouter.post("/filter-event")
def filterEvent(event: EventFiltersSchema):
    response = TypeUtilities.parse_json(eventService.get_events_by_filter(event))
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)