import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from app.main import app
from app.state import queues, app_state
from app.workers import process_events

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_state():
    """Reset queues and state before each test"""
    app_state["shutting_down"] = False
    for q in queues.values():
        while not q.empty():
            q.get_nowait()
            q.task_done()


def test_valid_event_submission():
    payload = {
        "eventType": "EMAIL",
        "payload": {"recipient": "test@test.com"},
        "callbackUrl": "http://client.com/cb"
    }
    response = client.post("/api/events", json=payload)
    assert response.status_code == 202
    assert "eventId" in response.json()
    assert queues["EMAIL"].qsize() == 1

def test_invalid_event_type():
    payload = {
        "eventType": "PIGEON", 
        "payload": {},
        "callbackUrl": "http://client.com/cb"
    }
    response = client.post("/api/events", json=payload)
    assert response.status_code == 400

def test_missing_payload_fields():
    response = client.post("/api/events", json={"eventType": "EMAIL"})
    assert response.status_code == 422 


@pytest.mark.asyncio
@patch('random.random')
@patch('httpx.AsyncClient.post')
async def test_event_processing_success(mock_post, mock_random):
    mock_random.return_value = 0.5
    mock_post.return_value = AsyncMock()

    event_data = {"eventId": "test-id-123", "callbackUrl": "http://client.com/cb"}
    await queues["PUSH"].put(event_data)
    
    worker_task = asyncio.create_task(process_events("PUSH"))
    
    await queues["PUSH"].join()
    worker_task.cancel()
    
    mock_post.assert_called_once()
    called_kwargs = mock_post.call_args[1]
    assert called_kwargs['json']['status'] == "COMPLETED"
    assert called_kwargs['json']['eventType'] == "PUSH"

@pytest.mark.asyncio
@patch('random.random')
@patch('httpx.AsyncClient.post')
async def test_event_processing_failure(mock_post, mock_random):
    mock_random.return_value = 0.05 # for mocking failure
    mock_post.return_value = AsyncMock()

    event_data = {"eventId": "test-fail-123", "callbackUrl": "http://client.com/cb"}
    await queues["SMS"].put(event_data)
    
    worker_task = asyncio.create_task(process_events("SMS"))
    
    await queues["SMS"].join()
    worker_task.cancel()
    
    mock_post.assert_called_once()
    called_kwargs = mock_post.call_args[1]
    assert called_kwargs['json']['status'] == "FAILED"
    assert "errorMessage" in called_kwargs['json']

def test_graceful_shutdown_blocks_events():
    app_state["shutting_down"] = True
    payload = {"eventType": "EMAIL", "payload": {}, "callbackUrl": "http://client.com/cb"}
    response = client.post("/api/events", json=payload)
    assert response.status_code == 503