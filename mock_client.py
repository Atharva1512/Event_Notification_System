from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/my-webhook-receiver")
async def receive_callback(request: Request):
    # This reads the JSON data sent by your Event System
    data = await request.json()
    
    print("\n" + "="*50)
    print("🚨 INCOMING CALLBACK RECEIVED! 🚨")
    print(f"Event ID: {data.get('eventId')}")
    print(f"Status:   {data.get('status')}")
    print(f"Type:     {data.get('eventType')}")
    print("="*50 + "\n")
    
    return {"message": "Thanks, Event System! I got the update."}