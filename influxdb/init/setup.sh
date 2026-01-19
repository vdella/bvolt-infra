#!/bin/bash
set -e

influx auth create \
  --org "$DOCKER_INFLUXDB_INIT_ORG" \
  --read-bucket "$DOCKER_INFLUXDB_INIT_BUCKET" \
  --description "grafana-read-token"
