import asyncio

from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from dags.dag_factory import create_dag
from dataweave.gpt.batch_status_checker import batch_status_checker


def open_api_batch_status_check():
    asyncio.run(batch_status_checker.check_and_update_batch_states())


dag_id = "batch_status_check_dag"
schedule_interval = "*/10 * * * *"

task_definitions = [
    {
        "task_id": "batch_status_check_task",
        "operator": PythonOperator,
        "callable": open_api_batch_status_check,
        "op_kwargs": {},
    },
    {
        "task_id": "trigger_completed_batch_handler_dag",
        "operator": TriggerDagRunOperator,
        "callable": None,
        "op_kwargs": {
            "trigger_dag_id": "completed_batch_handler_dag",
        },
    },
]

batch_status_check_dag = create_dag(
    dag_id=dag_id,
    schedule_interval=schedule_interval,
    task_definitions=task_definitions,
)

globals()[dag_id] = batch_status_check_dag
