"""
Centralized application settings.

Loads configuration from environment variables and .env file.
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Project root directory (predictive-maintenance/)
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── API Server ───────────────────────────────
    api_host: str = "127.0.0.1"
    api_port: int = 8000

    # ── Model ────────────────────────────────────
    model_path: str = "models/predictive_maintenance_model.pkl"

    # ── Logging ──────────────────────────────────
    log_level: str = "INFO"

    # ── Dashboard ────────────────────────────────
    dashboard_port: int = 8501

    @property
    def model_abs_path(self) -> Path:
        """Resolve model path relative to the project root."""
        path = Path(self.model_path)
        if path.is_absolute():
            return path
        return BASE_DIR / path


# Singleton settings instance
settings = Settings()
