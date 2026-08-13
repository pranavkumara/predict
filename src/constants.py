"""
Shared constants used across the application.
"""

# ── Feature columns expected by the model ────────
FEATURE_COLUMNS = [
    "Air_temperature_K",
    "Process_temperature_K",
    "Rotational_speed_rpm",
    "Torque_Nm",
    "Tool_wear_min",
    "Type_L",
    "Type_M",
]

# ── Machine types ────────────────────────────────
MACHINE_TYPES = ("L", "M", "H")

# ── Risk level thresholds ────────────────────────
RISK_HIGH_THRESHOLD = 0.70
RISK_MEDIUM_THRESHOLD = 0.40

# ── Risk labels & recommendations ────────────────
RISK_LEVELS = {
    "HIGH": {
        "label": "HIGH",
        "recommendation": (
            "Schedule maintenance inspection immediately."
        ),
    },
    "MEDIUM": {
        "label": "MEDIUM",
        "recommendation": (
            "Monitor machine condition and "
            "consider preventive maintenance."
        ),
    },
    "LOW": {
        "label": "LOW",
        "recommendation": (
            "Machine operating normally. "
            "Continue regular monitoring."
        ),
    },
}
