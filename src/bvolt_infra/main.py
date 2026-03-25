from datetime import datetime
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx

from bvolt_infra import config
from bvolt_infra.core_client import CoreApiClient


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="bvolt-infra", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.allowed_origins,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
core_client = CoreApiClient()


@app.get("/")
async def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "core_source_label": config.core_source_label,
            "refresh_seconds": int(config.dashboard_refresh_seconds),
            "grafana_dashboard_title": config.grafana_dashboard_title,
            "grafana_embed_url": config.grafana_embed_url,
        },
    )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "bvolt-infra",
        "mode": "read-only",
        "core_base_url": config.core_base_url,
    }


@app.get("/api/inverters/latest")
async def latest():
    try:
        payload = await core_client.latest()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="Failed to connect to bvolt-core.") from exc
    return JSONResponse(payload)


@app.get("/api/inverters/timeseries")
async def timeseries(
        start: str = Query(..., description="ISO-8601 datetime"),
        end: str = Query(..., description="ISO-8601 datetime"),
):
    try:
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="start/end must be ISO-8601 datetimes.") from exc

    try:
        payload = await core_client.timeseries(start=start_dt, end=end_dt)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="Failed to connect to bvolt-core.") from exc
    return JSONResponse(payload)


def main() -> None:
    uvicorn.run(
        "bvolt_infra.main:app",
        host=config.app_host,
        port=config.app_port,
        reload=False,
    )


if __name__ == "__main__":
    main()
