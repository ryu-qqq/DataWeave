from airflow import DAG
from airflow.operators.python import PythonOperator
from dags.default_args import default_args
from dataweave.processor.batch_status_checker import batch_status_checker


def open_api_batch_status_check():
    batch_status_checker.check_and_update_batch_states()


with DAG(
        dag_id="open_api_batch_status_check",
        default_args=default_args(),
        schedule_interval="*/10 * * * *",
        catchup=False,
) as dag:
    fetch_config_task = PythonOperator(
        task_id="open_api_batch_status_check",
        python_callable=open_api_batch_status_check,
    )
