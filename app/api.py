import uuid
from fastapi import APIRouter, HTTPException, status
from app.models import EventRequest, EventResponse
from app.state import app_state, EVENT_CONFIG, queues

router = APIRouter()

@router.post("/api/events", response_model=EventResponse, status_code=status.HTTP_202_ACCEPTED)
async def add_new_event(request: EventRequest):
    if app_state["shutting_down"]:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="System is shutting down and not accepting new events."
        )

    if request.eventType not in EVENT_CONFIG:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid eventType. Must be EMAIL, SMS, or PUSH."
        )

    event_id = f"e{uuid.uuid4().hex[:8]}"
    
    event_data = {
        "eventId": event_id,
        "eventType": request.eventType,
        "payload": request.payload,
        "callbackUrl": request.callbackUrl
    }
    
    await queues[request.eventType].put(event_data)
    
    return EventResponse(eventId=event_id, message="Event accepted for processing.")