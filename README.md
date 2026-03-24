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

For a public deployment, point `BVOLT_CORE_BASE_URL` at an address reachable from the app process.
If `bvolt-infra` runs in Docker on the same network as `bvolt-core`, use the backend service name instead of `localhost`, for example `http://bvolt-core:8000`.

## Docker

`bvolt-infra` is deployed separately from `bvolt-core`.

Create the shared Docker network once:

```bash
docker network create bvolt-shared
```

Start this project:

```bash
docker compose up --build -d
```

This stack expects `bvolt-core` to already be running on the same `bvolt-shared` network.

## Environment

- `BVOLT_CORE_BASE_URL` default: `http://bvolt-core:8000`
- `BVOLT_CORE_API_KEY` default: unset
- `BVOLT_CORE_SOURCE_LABEL` default: `Internal bvolt-core service`
- `BVOLT_ALLOWED_ORIGINS` default: `*`
- `DASHBOARD_REFRESH_SECONDS` default: `5`
- `BVOLT_APP_HOST` default: `0.0.0.0`
- `BVOLT_APP_PORT` default: `8010`

## Notes

- This starter intentionally does not write data.
- Keep `bvolt-core` running and reachable from this app.
- The browser only talks to `bvolt-infra`; upstream access stays server-side, which is what makes public viewing possible.
- If `BVOLT_CORE_API_KEY` is set, `bvolt-infra` sends it upstream as the `X-API-Key` header.
