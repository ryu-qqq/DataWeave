from airflow.operators.python import PythonOperator

from dags.dag_factory import create_dag
from dataweave.gpt.batch_process_manager import batch_processor_manager


def open_api_batch_result_handle():
    batch_processor_manager.process_completed_batches()


dag_id = "batch_result_handling_dag"
schedule_interval = "*/15 * * * *"

task_definitions = [
    {
        "task_id": "open_api_batch_manage_task",
        "operator": PythonOperator,
        "callable": open_api_batch_result_handle,
        "op_kwargs": {}
    }
]

batch_result_handling_dag = create_dag(
    dag_id=dag_id,
    schedule_interval=schedule_interval,
    task_definitions=task_definitions
)

globals()[dag_id] = batch_result_handling_dag
