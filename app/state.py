import asyncio

EVENT_CONFIG = {
    "EMAIL": {"processing_time": 5},
    "SMS": {"processing_time": 3},
    "PUSH": {"processing_time": 2},
}

# The shared queues that both the API (producer) and workers (consumers) will use
queues = {
    "EMAIL": asyncio.Queue(),
    "SMS": asyncio.Queue(),
    "PUSH": asyncio.Queue(),
}

workers = []
app_state = {"shutting_down": False}