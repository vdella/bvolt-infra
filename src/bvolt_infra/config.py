import os

from dotenv import load_dotenv

load_dotenv()


def _get_float(name: str, default: float) -> float:
    value = os.getenv(name)
    return float(value) if value is not None else default


core_base_url = os.getenv("BVOLT_CORE_BASE_URL", "http://localhost:8000").rstrip("/")
dashboard_refresh_seconds = _get_float("DASHBOARD_REFRESH_SECONDS", 5.0)
