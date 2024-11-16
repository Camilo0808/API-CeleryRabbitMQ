# FastAPI Task Processor with RabbitMQ and Celery

This is a simple backend application built with FastAPI that demonstrates how to use RabbitMQ and Celery for asynchronous task processing. The application is containerized using Docker Compose.

## Features
- Submit tasks with a payload to be processed asynchronously.
- Check the status and result of submitted tasks.
- Uses Celery with RabbitMQ as the message broker and backend.
- Follows security practices for containerized environments.

---

## Requirements
- Docker
- Docker Compose

---

## Getting Started
### 1. Clone the repository:
```bash
git clone https://github.com/Camilo0808/API-CeleryRabbitMQ
cd API-CeleryRabbitMQ
```

### 2. Build and run the services:
```bash
docker-compose up --build
```

- The API will be available at `http://localhost:8000`
- RabbitMQ Management UI will be available at `http://localhost:15672` (username: `guest`, password: `guest`)

---

## Endpoints
### POST `/tasks`
Create a new task.

#### Request Body
```json
{
  "task_name": "example_task",
  "payload": {
    "key": "value"
  }
}
```
#### Response
```json
{
  "task_id": "<task_id>",
  "status": "Task submitted"
}
```

### GET `/tasks/{task_id}`
Retrieve the status and result of a task by its ID.

#### Response (Pending)
```json
{
  "task_id": "<task_id>",
  "status": "PENDING",
  "result": null
}
```

#### Response (Success)
```json
{
  "task_id": "<task_id>",
  "status": "SUCCESS",
  "result": {
    "task_name": "example_task",
    "processed_data": {
      "key": "value"
    }
  }
}
```

---

## Project Structure
```
.
├── app
│   ├── Dockerfile
│   ├── main.py
├── docker-compose.yml
├── LICENSE
├── requirements.txt
└── README.md
```

---

## Security Practices
- **Environment Variables**: All sensitive data like broker URLs are stored in environment variables.
- **Dependency Management**: Minimal dependencies are used to reduce the attack surface.
- **Container Isolation**: Each service runs in its own container.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.
