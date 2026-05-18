from datetime import datetime
import sys

sys.path.append('/opt/airflow/etl')

from airflow import DAG
from airflow.operators.python import PythonOperator

from extract import extract_orders
from transform import transform_orders
from load import load_to_clickhouse


def run_etl():

    raw_data = extract_orders()

    transformed_data = transform_orders(raw_data)

    load_to_clickhouse(transformed_data)


with DAG(
   dag_id="orders_etl_pipeline",
   start_date=datetime(2026, 1, 1),
   schedule="*/5 * * * *",
   catchup=False,
   tags=["mci"]
) as dag:

    run_pipeline = PythonOperator(
        task_id="run_etl_pipeline",
        python_callable=run_etl
    )