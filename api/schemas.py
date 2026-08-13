"""
Pydantic schemas for the Predictive Maintenance API.
"""

from typing import Literal

from pydantic import BaseModel, Field


class MachineInput(BaseModel):
    """Input schema for machine sensor readings."""

    machine_type: Literal["L", "M", "H"] = Field(
        ...,
        description="Machine quality type: L (Low), M (Medium), or H (High)",
    )

    air_temperature: float = Field(
        ...,
        ge=250.0,
        le=350.0,
        description="Air temperature in Kelvin",
    )

    process_temperature: float = Field(
        ...,
        ge=250.0,
        le=400.0,
        description="Process temperature in Kelvin",
    )

    rotational_speed: float = Field(
        ...,
        ge=0.0,
        le=5000.0,
        description="Rotational speed in RPM",
    )

    torque: float = Field(
        ...,
        ge=0.0,
        le=200.0,
        description="Torque in Nm",
    )

    tool_wear: float = Field(
        ...,
        ge=0.0,
        le=300.0,
        description="Tool wear in minutes",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "machine_type": "M",
                    "air_temperature": 298.1,
                    "process_temperature": 308.6,
                    "rotational_speed": 1551.0,
                    "torque": 42.8,
                    "tool_wear": 0.0,
                }
            ]
        }
    }


class PredictionResponse(BaseModel):
    """Response schema for failure prediction results."""

    prediction: int = Field(
        ...,
        description="0 = No failure predicted, 1 = Failure predicted",
    )

    failure_probability: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Probability of machine failure (0.0 to 1.0)",
    )

    risk_level: Literal["LOW", "MEDIUM", "HIGH"] = Field(
        ...,
        description="Risk classification based on failure probability",
    )

    recommendation: str = Field(
        ...,
        description="Maintenance recommendation based on risk level",
    )


class HealthResponse(BaseModel):
    """Response schema for the health check endpoint."""

    status: str
    model_loaded: bool
    threshold: float | None = None