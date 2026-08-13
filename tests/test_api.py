"""Tests for the FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture(scope="module")
def client():
    """Create a test client with lifespan events."""
    with TestClient(app) as c:
        yield c


# --------------------------------------------------
# Root endpoint
# --------------------------------------------------

class TestRootEndpoint:
    """Test the root (/) endpoint."""

    def test_root_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_root_contains_message(self, client):
        data = client.get("/").json()
        assert "message" in data
        assert "Predictive Maintenance" in data["message"]

    def test_root_contains_threshold(self, client):
        data = client.get("/").json()
        assert "threshold" in data
        assert data["threshold"] is not None


# --------------------------------------------------
# Health endpoint
# --------------------------------------------------

class TestHealthEndpoint:
    """Test the /health endpoint."""

    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_model_loaded(self, client):
        data = client.get("/health").json()
        assert data["status"] == "healthy"
        assert data["model_loaded"] is True


# --------------------------------------------------
# Predict endpoint
# --------------------------------------------------

VALID_PAYLOAD = {
    "machine_type": "M",
    "air_temperature": 298.1,
    "process_temperature": 308.6,
    "rotational_speed": 1551.0,
    "torque": 42.8,
    "tool_wear": 0.0,
}


class TestPredictEndpoint:
    """Test the /predict endpoint."""

    def test_predict_returns_200(self, client):
        response = client.post("/predict", json=VALID_PAYLOAD)
        assert response.status_code == 200

    def test_predict_response_fields(self, client):
        data = client.post("/predict", json=VALID_PAYLOAD).json()
        assert "prediction" in data
        assert "failure_probability" in data
        assert "risk_level" in data
        assert "recommendation" in data

    def test_predict_prediction_is_binary(self, client):
        data = client.post("/predict", json=VALID_PAYLOAD).json()
        assert data["prediction"] in (0, 1)

    def test_predict_probability_in_range(self, client):
        data = client.post("/predict", json=VALID_PAYLOAD).json()
        assert 0.0 <= data["failure_probability"] <= 1.0

    def test_predict_risk_level_valid(self, client):
        data = client.post("/predict", json=VALID_PAYLOAD).json()
        assert data["risk_level"] in ("LOW", "MEDIUM", "HIGH")

    def test_predict_invalid_machine_type(self, client):
        bad_payload = {**VALID_PAYLOAD, "machine_type": "X"}
        response = client.post("/predict", json=bad_payload)
        assert response.status_code == 422

    def test_predict_missing_field(self, client):
        incomplete = {
            "machine_type": "M",
            "air_temperature": 298.1,
        }
        response = client.post("/predict", json=incomplete)
        assert response.status_code == 422

    def test_predict_temperature_out_of_range(self, client):
        bad_payload = {**VALID_PAYLOAD, "air_temperature": 100.0}
        response = client.post("/predict", json=bad_payload)
        assert response.status_code == 422
