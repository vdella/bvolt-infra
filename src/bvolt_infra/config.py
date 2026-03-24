import os

from dotenv import load_dotenv

load_dotenv()


def _get_float(name: str, default: float) -> float:
    value = os.getenv(name)
    return float(value) if value is not None else default


def _get_list(name: str, default: list[str]) -> list[str]:
    value = os.getenv(name)
    if value is None:
        return default
    return [item.strip() for item in value.split(",") if item.strip()]


core_base_url = os.getenv("BVOLT_CORE_BASE_URL", "http://localhost:8000").rstrip("/")
core_api_key = os.getenv("BVOLT_CORE_API_KEY")
core_source_label = os.getenv("BVOLT_CORE_SOURCE_LABEL", "Internal bvolt-core service")
dashboard_refresh_seconds = _get_float("DASHBOARD_REFRESH_SECONDS", 5.0)
allowed_origins = _get_list("BVOLT_ALLOWED_ORIGINS", ["*"])
app_host = os.getenv("BVOLT_APP_HOST", "0.0.0.0")
app_port = int(os.getenv("BVOLT_APP_PORT", "8010"))
