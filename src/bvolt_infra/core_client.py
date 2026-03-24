from collections.abc import Mapping
from datetime import datetime
from typing import Any

import httpx

from bvolt_infra import config


class CoreApiClient:
    def __init__(self, base_url: str | None = None, timeout_seconds: float = 8.0) -> None:
        self._base_url = (base_url or config.core_base_url).rstrip("/")
        self._timeout_seconds = timeout_seconds

    async def latest(self) -> Mapping[str, Any]:
        url = f"{self._base_url}/inverter"
        async with httpx.AsyncClient(timeout=self._timeout_seconds) as client:
            response = await client.get(url)
        response.raise_for_status()
        return response.json()

    async def timeseries(self, start: datetime, end: datetime) -> Mapping[str, Any]:
        url = f"{self._base_url}/inverter/timeseries"
        params = {"start": start.isoformat(), "end": end.isoformat()}
        async with httpx.AsyncClient(timeout=self._timeout_seconds) as client:
            response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()
