from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_healthcheck():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_error():
    response = client.post("/predict", json={"executions": []})
    assert response.status_code == 400
    assert response.json() == {"detail": "No execution data provided"}


def test_predict_wrong_schema():
    response = client.post("/predict", json={"executions": [
        {
            "tenant_name": "SETH",
            "task_id": "prepare_campaigns_basic_settings",
            "start_date_time": "2024-08-20 13:14:38.581"
        }
    ]})
    assert response.status_code == 422


def test_correct_schema():
    response = client.post("/predict", json={"executions": [
        {
            "tenant_name": "SETH",
            "task_id": "prepare_campaigns_basic_settings",
            "start_date_time": "2024-08-20 13:14:38.581",
            "duration": 7.904338,
            "warehouse_size": "X-Small",
            "number_of_campaigns": 114,
            "number_of_customers": 22719259
        }
    ]})
    assert response.status_code == 200
