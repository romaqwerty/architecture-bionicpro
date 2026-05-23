#!/usr/bin/env bash
set -euo pipefail

airflow db init

if airflow users list | awk '{print $2}' | grep -qx "admin"; then
  echo "Airflow user 'admin' already exists. Skipping creation."
else
  airflow users create \
    --username admin \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@sample.ru \
    --password admin
fi

bash /opt/airflow/scripts/init-connections.sh
