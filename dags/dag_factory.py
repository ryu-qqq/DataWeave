from datetime import datetime
from airflow import DAG

from dags.dag_result_callback import global_on_success_callback, global_on_failure_callback


def create_dag(dag_id: str, schedule_interval: str = None, task_definitions: list = None) -> DAG:
    default_args = create_default_args()

    with DAG(
            dag_id=dag_id,
            default_args=default_args,
            schedule_interval=schedule_interval,
            catchup=False,
    ) as dag:
        if task_definitions:
            previous_task = None
            for task_def in task_definitions:
                task = task_def["operator"](
                    task_id=task_def["task_id"],
                    python_callable=task_def["callable"],
                    op_kwargs=task_def.get("op_kwargs", {}),
                    provide_context=True
                )
                if previous_task:
                    task.set_upstream(previous_task)
                previous_task = task

    return dag


def create_default_args(
        owner='ryuqq',
        depends_on_past=False,
        start_date=None,
        retries=1,
        email_on_failure=False,
        email_on_retry=False,
        retry_delay=None
):
    default_args = {
        'owner': owner,
        'depends_on_past': depends_on_past,
        'start_date': start_date or datetime(2024, 12, 27),
        'retries': retries,
        'email_on_failure': email_on_failure,
        'email_on_retry': email_on_retry,
        'on_success_callback': global_on_success_callback,
        'on_failure_callback': global_on_failure_callback,
    }

    if retry_delay:
        default_args['retry_delay'] = retry_delay

    return default_args
