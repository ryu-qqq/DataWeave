from airflow import DAG
from airflow.operators.python import PythonOperator

from dags.default_args import default_args
from dataweave.processor.batch_process_manager import batch_processor_manager


def open_api_batch_process():
    batch_processor_manager.process_completed_batches()


with DAG(
        dag_id="open_api_batch_process",
        default_args=default_args(),
        schedule_interval="*/20 * * * *",
        catchup=False,
) as dag:
    fetch_config_task = PythonOperator(
        task_id="open_api_batch_process",
        python_callable=open_api_batch_process,
    )
