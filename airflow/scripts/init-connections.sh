#!/usr/bin/env bash
set -euo pipefail

create_connection_if_not_exists() {
  local conn_id=${1:?Connection id is required}
  shift

  if airflow connections get "$conn_id" >/dev/null 2>&1; then
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] INFO: Connection '$conn_id' already exists. Skipping creation."
    return 0
  fi

  echo "[$(date +'%Y-%m-%d %H:%M:%S')] INFO: Creating connection '$conn_id'..."

  airflow connections add "$conn_id" "$@"
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] INFO: Connection '$conn_id' created successfully."
}

create_connection_if_not_exists crm_pg \
  --conn-type postgres \
  --conn-host postgres \
  --conn-login airflow \
  --conn-password airflow \
  --conn-port 5432 \
  --conn-schema crm

create_connection_if_not_exists telemetry_pg \
  --conn-type postgres \
  --conn-host postgres \
  --conn-login airflow \
  --conn-password airflow \
  --conn-port 5432 \
  --conn-schema telemetry

create_connection_if_not_exists olap_pg \
  --conn-type postgres \
  --conn-host postgres \
  --conn-login airflow \
  --conn-password airflow \
  --conn-port 5432 \
  --conn-schema olap
