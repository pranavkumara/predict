"""Tests for Pydantic schemas."""

import pytest
from pydantic import ValidationError

from api.schemas import MachineInput, PredictionResponse


# --------------------------------------------------
# MachineInput — valid cases
# --------------------------------------------------

class TestMachineInputValid:
    """Test that valid inputs are accepted."""

    def test_valid_input(self):
        data = MachineInput(
            machine_type="M",
            air_temperature=298.1,
            process_temperature=308.6,
            rotational_speed=1551.0,
            torque=42.8,
            tool_wear=0.0,
        )
        assert data.machine_type == "M"
        assert data.air_temperature == 298.1

    @pytest.mark.parametrize("machine_type", ["L", "M", "H"])
    def test_all_machine_types(self, machine_type):
        data = MachineInput(
            machine_type=machine_type,
            air_temperature=300.0,
            process_temperature=310.0,
            rotational_speed=1500.0,
            torque=40.0,
            tool_wear=100.0,
        )
        assert data.machine_type == machine_type

    def test_boundary_values(self):
        """Test minimum and maximum boundary values."""
        data = MachineInput(
            machine_type="L",
            air_temperature=250.0,
            process_temperature=250.0,
            rotational_speed=0.0,
            torque=0.0,
            tool_wear=0.0,
        )
        assert data.air_temperature == 250.0


# --------------------------------------------------
# MachineInput — invalid cases
# --------------------------------------------------

class TestMachineInputInvalid:
    """Test that invalid inputs are rejected."""

    def test_invalid_machine_type(self):
        with pytest.raises(ValidationError):
            MachineInput(
                machine_type="X",
                air_temperature=300.0,
                process_temperature=310.0,
                rotational_speed=1500.0,
                torque=40.0,
                tool_wear=100.0,
            )

    def test_temperature_too_low(self):
        with pytest.raises(ValidationError):
            MachineInput(
                machine_type="M",
                air_temperature=100.0,  # below 250
                process_temperature=310.0,
                rotational_speed=1500.0,
                torque=40.0,
                tool_wear=100.0,
            )

    def test_negative_torque(self):
        with pytest.raises(ValidationError):
            MachineInput(
                machine_type="M",
                air_temperature=300.0,
                process_temperature=310.0,
                rotational_speed=1500.0,
                torque=-10.0,
                tool_wear=100.0,
            )

    def test_missing_field(self):
        with pytest.raises(ValidationError):
            MachineInput(
                machine_type="M",
                air_temperature=300.0,
                # missing process_temperature
                rotational_speed=1500.0,
                torque=40.0,
                tool_wear=100.0,
            )


# --------------------------------------------------
# PredictionResponse
# --------------------------------------------------

class TestPredictionResponse:
    """Test the prediction response schema."""

    def test_valid_response(self):
        resp = PredictionResponse(
            prediction=1,
            failure_probability=0.85,
            risk_level="HIGH",
            recommendation="Schedule maintenance.",
        )
        assert resp.prediction == 1
        assert resp.risk_level == "HIGH"

    def test_invalid_risk_level(self):
        with pytest.raises(ValidationError):
            PredictionResponse(
                prediction=0,
                failure_probability=0.1,
                risk_level="UNKNOWN",
                recommendation="Some text.",
            )
