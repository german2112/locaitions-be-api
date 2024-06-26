from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional

class JoinEventRequestStatus(Enum):
        sent = "Sent"
        rejected = "Rejected"
        accepted = "Accepted"

class JoinEventRequest(BaseModel):
    event_id: str = Field(
        description="This is the id of the event thay is being requested to join")
    user_uid: str = Field(description="User id")
    status: JoinEventRequestStatus = Field(
        default=JoinEventRequestStatus.sent.value)
    last_updated: Optional[datetime] = Field(
        default=datetime.now(ZoneInfo('utc')))
