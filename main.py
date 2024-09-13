from datetime import datetime
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from classifier import Classifier

app = FastAPI(title="Warehouse size classifier")
wh_classifier = Classifier()


class TaskExecution(BaseModel):
    tenant_name: str
    task_id: str
    start_date_time: Optional[datetime]
    duration: float
    warehouse_size: Optional[str]
    number_of_campaigns: int
    number_of_customers: int


class TaskExecutionRequest(BaseModel):
    executions: List[TaskExecution]


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/predict", response_model=Dict[str, str])
async def predict_warehouses(request: TaskExecutionRequest):
    if not request.executions:
        raise HTTPException(status_code=400, detail="No execution data provided")

    return wh_classifier.predict_all(request.executions)
