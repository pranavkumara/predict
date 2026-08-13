"""
FastAPI application for predictive maintenance.

Provides endpoints for machine failure prediction
using a trained XGBoost model.
"""

import logging
from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.schemas import HealthResponse, MachineInput, PredictionResponse
from config.settings import settings
from src.constants import RISK_HIGH_THRESHOLD, RISK_LEVELS, RISK_MEDIUM_THRESHOLD
from src.model_loader import ModelPackage, load_model

# ── Logging ──────────────────────────────────────

logging.basicConfig(
    level=settings.log_level.upper(),
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


# ── Model (populated at startup) ─────────────────

model_package: ModelPackage | None = None


# ── Lifespan ─────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the model on startup; clean up on shutdown."""
    global model_package

    logger.info("Starting up — loading model...")
    model_package = load_model(settings.model_abs_path)
    logger.info("Model ready.")

    yield  # Application runs here

    logger.info("Shutting down.")
    model_package = None


# ── FastAPI app ──────────────────────────────────

app = FastAPI(
    title="Predictive Maintenance API",
    description="Machine failure prediction using XGBoost",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ─────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Endpoints
# --------------------------------------------------

@app.get("/")
def root():
    """Root endpoint — confirms the API is running."""
    return {
        "message": "Predictive Maintenance API is running",
        "model": "XGBoost",
        "threshold": (
            model_package.threshold if model_package else None
        ),
    }


@app.get("/health", response_model=HealthResponse)
def health():
    """Health check for readiness probes."""
    return HealthResponse(
        status="healthy" if model_package else "unavailable",
        model_loaded=model_package is not None,
        threshold=(
            model_package.threshold if model_package else None
        ),
    )


@app.post("/predict", response_model=PredictionResponse)
def predict(machine: MachineInput):
    """Predict whether a machine is likely to fail."""

    if model_package is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded yet.",
        )

    try:
        # ── Build input dataframe ────────────────
        input_data = pd.DataFrame(
            {
                "Air_temperature_K": [machine.air_temperature],
                "Process_temperature_K": [machine.process_temperature],
                "Rotational_speed_rpm": [machine.rotational_speed],
                "Torque_Nm": [machine.torque],
                "Tool_wear_min": [machine.tool_wear],
            }
        )

        # ── Encode machine type ──────────────────
        input_data["Type_L"] = machine.machine_type == "L"
        input_data["Type_M"] = machine.machine_type == "M"

        # ── Ensure correct feature order ─────────
        input_data = input_data[model_package.features]

        # ── Predict ──────────────────────────────
        probability = model_package.model.predict_proba(
            input_data
        )[0, 1]

        prediction = int(probability >= model_package.threshold)

        # ── Risk level ───────────────────────────
        if probability >= RISK_HIGH_THRESHOLD:
            risk_info = RISK_LEVELS["HIGH"]
        elif probability >= RISK_MEDIUM_THRESHOLD:
            risk_info = RISK_LEVELS["MEDIUM"]
        else:
            risk_info = RISK_LEVELS["LOW"]

        logger.info(
            "Prediction: prob=%.4f, risk=%s, type=%s",
            probability,
            risk_info["label"],
            machine.machine_type,
        )

        return PredictionResponse(
            prediction=prediction,
            failure_probability=round(float(probability), 4),
            risk_level=risk_info["label"],
            recommendation=risk_info["recommendation"],
        )

    except Exception:
        logger.exception("Prediction failed")
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred during prediction.",
        )