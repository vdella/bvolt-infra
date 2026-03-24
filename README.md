# bvolt-infra (starter)

Read-only application that consumes `bvolt-core` endpoints and serves a dashboard shell.

## What it does

- Calls `bvolt-core` `GET /inverter` and `GET /inverter/timeseries`.
- Exposes read-only proxy endpoints:
  - `GET /api/inverters/latest`
  - `GET /api/inverters/timeseries?start=<iso>&end=<iso>`
- Serves a basic dashboard UI at `GET /`.

## Setup

```bash
cd bvolt-infra
cp .env.example .env
uv sync
uv run python -m bvolt_infra.main
```

Default URL: `http://localhost:8010`

## Environment

- `BVOLT_CORE_BASE_URL` default: `http://localhost:8000`
- `DASHBOARD_REFRESH_SECONDS` default: `5`

## Notes

- This starter intentionally does not write data.
- Keep `bvolt-core` running and reachable from this app.
