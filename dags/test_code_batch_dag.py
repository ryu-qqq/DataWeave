import asyncio

from dags.dag_factory import create_dag
from airflow.operators.python import PythonOperator

from dataweave.enums.product_data_type import BatchDataType
from dataweave.enums.source_type import SourceType
from dataweave.gpt.batch_processor import batch_processor


def process_test_code_batches(**context):
    asyncio.run(batch_processor.process(
        source_type=SourceType.TEST_CODE,
        fetch_params={
            "status": "PENDING",
            "change_types": ["ADDED", "MODIFIED"],
            "page_size": 20,
            "page_number": 0,
            "cursor": None,
            "sort": "ASC"
        },
        batch_data_type=BatchDataType.TEST_CODE
    ))


dag_id = "test_code_batch_dag"
schedule_interval = "0 * * * *"

task_definitions = [
    {
        "task_id": "process_test_code_batches",
        "operator": PythonOperator,
        "callable": process_test_code_batches,
        "op_kwargs": {}
    }
]

# DAG 생성
test_code_batch_dag = create_dag(
    dag_id=dag_id,
    schedule_interval=schedule_interval,
    task_definitions=task_definitions
)

# DAG 등록
globals()[dag_id] = test_code_batch_dag
