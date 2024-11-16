# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from celery import Celery
import os

# Initialize FastAPI
app = FastAPI(title="Task Processor API", description="An example API using FastAPI, RabbitMQ, and Celery")

# Initialize Celery
celery = Celery(
    broker=os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@rabbitmq:5672//"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "rpc://")
)

# Task model
class TaskRequest(BaseModel):
    task_name: str
    payload: dict

# Celery Task
@celery.task
def process_task(task_name: str, payload: dict):
    # Simulate task processing
    return {"task_name": task_name, "processed_data": payload}

@app.post("/tasks", summary="Create a task", description="Send a task to be processed by Celery")
async def create_task(task_request: TaskRequest):
    try:
        task = process_task.apply_async(args=[task_request.task_name, task_request.payload])
        return {"task_id": task.id, "status": "Task submitted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks/{task_id}", summary="Get task result", description="Retrieve the result of a task using its ID")
async def get_task_result(task_id: str):
    try:
        task = process_task.AsyncResult(task_id)
        if task.state == "PENDING":
            return {"task_id": task.id, "status": task.state, "result": None}
        if task.state == "SUCCESS":
            return {"task_id": task.id, "status": task.state, "result": task.result}
        else:
            return {"task_id": task.id, "status": task.state, "result": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))