from pydantic import BaseModel, HttpUrl, Field
from typing import Dict, Any

class EventRequest(BaseModel):
    eventType: str = Field(..., description="Must be EMAIL, SMS, or PUSH")
    payload: Dict[str, Any]
    callbackUrl: HttpUrl

class EventResponse(BaseModel):
    eventId: str
    message: str