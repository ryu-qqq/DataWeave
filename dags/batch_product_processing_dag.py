from airflow import DAG
from airflow.operators.python import PythonOperator

from dags.default_args import default_args
from dataweave.processor.batch_processor import batch_processor


def open_api_batch_completed_handling():
    batch_processor.process(site_id=None, seller_id=None)


with DAG(
        dag_id="open_api_batch_completed_handling",
        default_args=default_args(),
        schedule_interval="*/30 * * * *",
        catchup=False,
) as dag:
    fetch_config_task = PythonOperator(
        task_id="open_api_batch_completed_handling",
        python_callable=open_api_batch_completed_handling,
    )
