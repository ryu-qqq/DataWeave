import asyncio

from airflow.operators.python import PythonOperator

from dags.dag_factory import create_dag
from dataweave.enums.product_data_type import BatchDataType
from dataweave.gpt.batch_processor import batch_processor


def process_product_batches():
    asyncio.run(batch_processor.process(
        fetch_params={
            "status": "PENDING",
            "change_types": ["ADDED", "MODIFIED"],
            "page_size": 20,
            "page_number": 0,
            "cursor": None,
            "sort": "ASC"
        },
        batch_data_type=BatchDataType.PRODUCT
    ))


dag_id = "product_batch_dag"
schedule_interval = "0 * * * *"

task_definitions = [
    {
        "task_id": "process_test_code_batches",
        "operator": PythonOperator,
        "callable": process_product_batches,
        "op_kwargs": {}
    }
]

product_batch_dag = create_dag(
    dag_id=dag_id,
    schedule_interval=schedule_interval,
    task_definitions=task_definitions
)

# DAG 등록
globals()[dag_id] = product_batch_dag
