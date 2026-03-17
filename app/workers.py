import asyncio
import random
import httpx
from datetime import datetime, timezone
from app.state import EVENT_CONFIG, queues

async def process_events(event_type: str):
    """Background worker to process events from a specific queue."""
    processing_time = EVENT_CONFIG[event_type]["processing_time"]
    queue = queues[event_type]
    
    async with httpx.AsyncClient() as client:
        while True:
            try:
                event = await queue.get()
                
                # Simulate processing
                await asyncio.sleep(processing_time)
                
                # Simulate 10% failure
                is_failed = random.random() < 0.10
                
                # Trigger callback
                callback_payload = {
                    "eventId": event["eventId"],
                    "status": "FAILED" if is_failed else "COMPLETED",
                    "eventType": event_type,
                    "processedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                }
                
                if is_failed:
                    callback_payload["errorMessage"] = "Simulated processing failure"

                try:
                    await client.post(str(event["callbackUrl"]), json=callback_payload)
                except httpx.RequestError as e:
                    print(f"[{event_type}] Callback failed for {event['eventId']}: {e}")


                queue.task_done()
            
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[{event_type}] Unexpected worker error: {e}")