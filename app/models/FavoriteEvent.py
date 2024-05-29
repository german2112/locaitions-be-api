from pydantic import BaseModel, Field
from datetime import datetime
from zoneinfo import ZoneInfo


class FavoriteEvent(BaseModel):
    event_id: str = Field(description="Id of the event marked as favorite")
    user_id: str = Field(
        description="Uid of the user that added this event to favorites")
    created_at: datetime = Field(default=datetime.now(ZoneInfo('UTC')))
