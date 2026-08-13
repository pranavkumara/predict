"""
Reusable model loader for the predictive maintenance model.

Encapsulates loading the pickled model package so that both
the FastAPI app and any future scripts/notebooks can use it.
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import joblib
import warnings

logger = logging.getLogger(__name__)


@dataclass
class ModelPackage:
    """Container for a loaded model and its metadata."""

    model: Any
    threshold: float
    features: list[str] = field(default_factory=list)


def load_model(model_path: Path) -> ModelPackage:
    """
    Load a pickled model package from disk.

    Parameters
    ----------
    model_path : Path
        Absolute or relative path to the .pkl file.

    Returns
    -------
    ModelPackage
        Dataclass holding the model, threshold, and feature list.

    Raises
    ------
    FileNotFoundError
        If the model file does not exist.
    """
    model_path = Path(model_path)

    if not model_path.exists():
        raise FileNotFoundError(
            f"Model file not found: {model_path}"
        )

    logger.info("Loading model from %s", model_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)
        package = joblib.load(model_path)

    model_pkg = ModelPackage(
        model=package["model"],
        threshold=package["threshold"],
        features=package["features"],
    )

    logger.info(
        "Model loaded successfully "
        "(threshold=%.4f, features=%d)",
        model_pkg.threshold,
        len(model_pkg.features),
    )

    return model_pkg
