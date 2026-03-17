import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.state import EVENT_CONFIG, queues, workers, app_state
from app.workers import process_events
from app.api import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create the workers
    for event_type in EVENT_CONFIG.keys():
        task = asyncio.create_task(process_events(event_type))
        workers.append(task)
    
    yield
    
    # Shutdown logic
    print("\nInitiating graceful shutdown...")
    app_state["shutting_down"] = True
    
    for event_type, queue in queues.items():
        print(f"Waiting for {event_type} queue to drain...")
        await queue.join()
        
    for task in workers:
        task.cancel()
    
    await asyncio.gather(*workers, return_exceptions=True)
    print("Shutdown complete.")

# Initialize app and include the routes from api.py
app = FastAPI(lifespan=lifespan)
app.include_router(router)