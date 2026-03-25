# bvolt-infra (starter)

Read-only application that consumes `bvolt-core` endpoints and serves a dashboard shell.

## What it does

- Calls `bvolt-core` `GET /inverter` and `GET /inverter/timeseries`.
- Exposes read-only proxy endpoints:
  - `GET /api/inverters/latest`
  - `GET /api/inverters/timeseries?start=<iso>&end=<iso>`
- Serves a basic dashboard UI at `GET /`.
- Can embed a Grafana dashboard in the same UI.

## Setup

```bash
cd bvolt-infra
cp .env.example .env
uv sync
uv run python -m bvolt_infra.main
```

Default URL: `http://localhost:8010`

This project now runs locally on the host. Keep `bvolt-core` running locally too and use:

```bash
BVOLT_CORE_BASE_URL=http://localhost:8000
```

Grafana remains containerized and is expected at `http://localhost:3000`.

## Docker

Docker is only used here for Grafana.

Create the shared Docker network once:

```bash
docker network create bvolt-shared
```

Start this project:

```bash
docker compose up -d
```

This starts only the Grafana container. `bvolt-infra` itself should be run with `uv run python -m bvolt_infra.main`.

## Environment

- `BVOLT_CORE_BASE_URL` default: `http://localhost:8000`
- `BVOLT_CORE_API_KEY` default: unset
- `BVOLT_CORE_SOURCE_LABEL` default: `Internal bvolt-core service`
- `BVOLT_ALLOWED_ORIGINS` default: `*`
- `DASHBOARD_REFRESH_SECONDS` default: `5`
- `BVOLT_APP_HOST` default: `0.0.0.0`
- `BVOLT_APP_PORT` default: `8010`
- `GRAFANA_BASE_URL` default: `http://localhost:3000`
- `GRAFANA_DASHBOARD_UID` default: `adxmk4pd`
- `GRAFANA_DASHBOARD_SLUG` default: `microgrid-integration-node`
- `GRAFANA_DASHBOARD_TITLE` default: `Grafana dashboard`
- `GRAFANA_ORG_ID` default: `1`
- `GRAFANA_KIOSK_MODE` default: `true`
- `GRAFANA_EMBED_URL` default: auto-built from the settings above

## Notes

- This starter intentionally does not write data.
- Keep `bvolt-core` running and reachable from this app.
- The browser only talks to `bvolt-infra`; upstream access stays server-side, which is what makes public viewing possible.
- If `BVOLT_CORE_API_KEY` is set, `bvolt-infra` sends it upstream as the `X-API-Key` header.
- Grafana in `docker-compose.yml` is configured for iframe embedding and anonymous viewer access so the dashboard can render inside `bvolt-infra`.
- Dashboards placed in `grafana/dashboards/` are auto-provisioned into Grafana on startup.
