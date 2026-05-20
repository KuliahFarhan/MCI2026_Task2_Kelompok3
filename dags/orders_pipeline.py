from datetime import datetime
import sys

sys.path.append('/opt/airflow/etl')

from airflow import DAG
from airflow.operators.python import PythonOperator

from extract import extract_orders
from transform import transform_orders
from load import load_to_clickhouse


def extract_task():
    return extract_orders()


def transform_task(**context):
    raw_data = context["ti"].xcom_pull(task_ids="extract_orders")
    return transform_orders(raw_data)


def load_task(**context):
    transformed_data = context["ti"].xcom_pull(task_ids="transform_orders")
    load_to_clickhouse(transformed_data)


with DAG(
    dag_id="orders_etl_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="*/5 * * * *",
    catchup=False,
    tags=["mci"]
) as dag:

    extract = PythonOperator(
        task_id="extract_orders",
        python_callable=extract_task
    )

    transform = PythonOperator(
        task_id="transform_orders",
        python_callable=transform_task
    )

    load = PythonOperator(
        task_id="load_to_clickhouse",
        python_callable=load_task
    )

    extract >> transform >> load