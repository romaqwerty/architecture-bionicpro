from datetime import datetime
from io import StringIO

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from sqlalchemy import text


CRM_CONN_ID = "crm_pg"
TELEMETRY_CONN_ID = "telemetry_pg"
OLAP_CONN_ID = "olap_pg"

USERS_XCOM_KEY = "users"
SENSORS_XCOM_KEY = "sensors"
REPORT_TABLE = "report"

USER_COLUMNS = ("id", "username", "email", "date_of_birth")
SENSOR_COLUMNS = ("user_id", "timestamp", "sensor_value")
REPORT_COLUMNS = (
    "username",
    "email",
    "date_of_birth",
    "timestamp",
    "sensor_value",
)

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 12, 1),
}


def read_postgres_table(
    conn_id: str,
    table_name: str,
    columns: tuple[str, ...],
) -> pd.DataFrame:
    query = f"SELECT {', '.join(columns)} FROM {table_name}"
    engine = PostgresHook(postgres_conn_id=conn_id).get_sqlalchemy_engine()
    return pd.read_sql(query, engine)


def push_dataframe(context: dict, key: str, df: pd.DataFrame) -> None:
    context["ti"].xcom_push(key=key, value=df.to_json(orient="records"))


def pull_dataframe(context: dict, task_id: str, key: str) -> pd.DataFrame:
    payload = context["ti"].xcom_pull(task_ids=task_id, key=key)
    return pd.read_json(StringIO(payload), orient="records")


def extract_users(**context) -> None:
    users_df = read_postgres_table(CRM_CONN_ID, "users", USER_COLUMNS)
    push_dataframe(context, USERS_XCOM_KEY, users_df)


def extract_sensor_data(**context) -> None:
    sensors_df = read_postgres_table(TELEMETRY_CONN_ID, "sensor_data", SENSOR_COLUMNS)
    push_dataframe(context, SENSORS_XCOM_KEY, sensors_df)


def build_report(**context) -> None:
    users_df = pull_dataframe(context, "extract_users", USERS_XCOM_KEY)
    sensors_df = pull_dataframe(context, "extract_sensor_data", SENSORS_XCOM_KEY)

    users_df = users_df.astype({"id": "string"})
    sensors_df = sensors_df.astype({"user_id": "string"})
    users_df["date_of_birth"] = pd.to_datetime(users_df["date_of_birth"], unit="ms")

    report_df = users_df.merge(
        sensors_df,
        left_on="id",
        right_on="user_id",
        how="inner",
    ).loc[:, REPORT_COLUMNS]

    engine = PostgresHook(postgres_conn_id=OLAP_CONN_ID).get_sqlalchemy_engine()
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {REPORT_TABLE}"))

    report_df.to_sql(REPORT_TABLE, engine, if_exists="append", index=False)


with DAG(
    dag_id="dag_crm_telemetry_report",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=["simple", "etl"],
) as dag:
    extract_users_task = PythonOperator(
        task_id="extract_users",
        python_callable=extract_users,
    )

    extract_sensor_data_task = PythonOperator(
        task_id="extract_sensor_data",
        python_callable=extract_sensor_data,
    )

    build_report_task = PythonOperator(
        task_id="build_report",
        python_callable=build_report,
    )

    [extract_users_task, extract_sensor_data_task] >> build_report_task
