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


def _get_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


core_base_url = os.getenv("BVOLT_CORE_BASE_URL", "http://localhost:8000").rstrip("/")
core_api_key = os.getenv("BVOLT_CORE_API_KEY")
core_source_label = os.getenv("BVOLT_CORE_SOURCE_LABEL", "Internal bvolt-core service")
dashboard_refresh_seconds = _get_float("DASHBOARD_REFRESH_SECONDS", 5.0)
allowed_origins = _get_list("BVOLT_ALLOWED_ORIGINS", ["*"])
app_host = os.getenv("BVOLT_APP_HOST", "0.0.0.0")
app_port = int(os.getenv("BVOLT_APP_PORT", "8010"))
grafana_base_url = os.getenv("GRAFANA_BASE_URL", "http://localhost:3000").rstrip("/")
grafana_dashboard_uid = os.getenv("GRAFANA_DASHBOARD_UID", "adxmk4pd")
grafana_dashboard_slug = os.getenv("GRAFANA_DASHBOARD_SLUG", "microgrid-integration-node").strip("/")
grafana_dashboard_title = os.getenv("GRAFANA_DASHBOARD_TITLE", "Grafana dashboard")
grafana_org_id = int(os.getenv("GRAFANA_ORG_ID", "1"))
grafana_kiosk_mode = _get_bool("GRAFANA_KIOSK_MODE", True)

_grafana_path = f"/d/{grafana_dashboard_uid}/{grafana_dashboard_slug}" if grafana_dashboard_uid else ""
_grafana_query = f"?orgId={grafana_org_id}"
if grafana_kiosk_mode:
    _grafana_query += "&kiosk"
_grafana_embed_url = os.getenv("GRAFANA_EMBED_URL", "").strip()
if _grafana_embed_url:
    grafana_embed_url = _grafana_embed_url
elif _grafana_path:
    grafana_embed_url = f"{grafana_base_url}{_grafana_path}{_grafana_query}"
else:
    grafana_embed_url = ""
