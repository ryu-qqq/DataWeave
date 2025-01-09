import asyncio
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from dataweave.gpt.completed_batch_handler import completed_batch_handler


def process_completed_batches():
    asyncio.run(completed_batch_handler.process_completed_batches())


dag_id = "completed_batch_handler_dag"

with DAG(
    dag_id=dag_id,
    default_args={
        "owner": "ryuqq",
        "start_date": datetime(2024, 12, 27),
        "catchup": False,
        "retries": 1,
    },
    schedule_interval=None,
) as completed_batch_handler_dag:
    task = PythonOperator(
        task_id="process_completed_batches_task",
        python_callable=process_completed_batches,
    )

globals()[dag_id] = completed_batch_handler_dag