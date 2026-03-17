# 🚀 Asynchronous Event Notification System

A robust, asynchronous, high-throughput Event Notification System built with **Python 3.11** and **FastAPI**. 

This system accepts notification requests (EMAIL, SMS, and PUSH) via a REST API, processes them asynchronously using strict FIFO (First-In, First-Out) memory queues, and fires a webhook callback to the client once processing succeeds or fails.

## 🛠️ Tech Stack
* **Framework:** FastAPI
* **Concurrency:** `asyncio` (Non-blocking workers and queues)
* **Testing:** `pytest` & `pytest-asyncio`
* **Containerization:** Docker & Docker Compose

---

## 📁 Project Structure

```text
event_system/
├── app/                  # Main application logic
│   ├── api.py            # REST API endpoints (Producer)
│   ├── main.py           # App entrypoint and Graceful Shutdown logic
│   ├── models.py         # Pydantic validation schemas
│   ├── state.py          # Global state (Queues, Config)
│   └── workers.py        # Background processors (Consumers)
├── tests/                # Automated test suite
│   └── test_api.py
├── mock_client.py        # Local webhook receiver for manual testing
├── Dockerfile
├── docker-compose.yml
└── requirements.txt

Gemini said
Here is a complete, professional README.md file for your project. It includes all the instructions for running the system via Docker or locally, spinning up the mock client, and executing your test suite.

You can copy this block exactly as it is and save it as README.md in the root of your event_system folder.

Markdown
# 🚀 Asynchronous Event Notification System

A robust, asynchronous, high-throughput Event Notification System built with **Python 3.11** and **FastAPI**. 

This system accepts notification requests (EMAIL, SMS, and PUSH) via a REST API, processes them asynchronously using strict FIFO (First-In, First-Out) memory queues, and fires a webhook callback to the client once processing succeeds or fails.

## 🛠️ Tech Stack
* **Framework:** FastAPI
* **Concurrency:** `asyncio` (Non-blocking workers and queues)
* **Testing:** `pytest` & `pytest-asyncio`
* **Containerization:** Docker & Docker Compose

---

## 📁 Project Structure

```text
event_system/
├── app/                  # Main application logic
│   ├── api.py            # REST API endpoints (Producer)
│   ├── main.py           # App entrypoint and Graceful Shutdown logic
│   ├── models.py         # Pydantic validation schemas
│   ├── state.py          # Global state (Queues, Config)
│   └── workers.py        # Background processors (Consumers)
├── tests/                # Automated test suite
│   └── test_api.py
├── mock_client.py        # Local webhook receiver for manual testing
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

⚙️ Getting Started
Prerequisites
Docker and Docker Compose (for containerized execution)

Python 3.11+ (for local execution and testing)

How to Run
1. Build the docker image and start the application on port 8080.
    ```bash
    docker compose up --build 
    ```
2. Start the Mock Webhook Receiver
    To see the callbacks in real-time, open a new terminal window and run the included mock client on port 8081 using:
    ```bash
    uvicorn mock_client:app --port 8081
    ```
3. Open Postman (or any other API Tool) -
    made POST method call one 
    http://localhost:8080/api/events
    with body like:
    ```json
    {
        "eventType": "SMS",
        "payload": {
            "phoneNumber": "+1234567890",
            "message": "Testing my local webhook!"
        },
        "callbackUrl": "http://host.docker.internal:8081/my-webhook-receiver"
    }
    ```