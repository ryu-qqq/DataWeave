import asyncio
import logging
from pathlib import Path
from prometheus_client import Counter
from airflow import DAG
from airflow.operators.python import PythonOperator

from dags.dag_factory import create_default_args
from dataweave.api_client.models.site_context_response import SiteContextResponse
from dataweave.api_client.models.site_profile_reponse import SiteProfileResponse
from dataweave.api_client.models.crawl_task_reponse import CrawlTaskResponse
from dataweave.task_executor import TaskExecutor

dags_created = Counter('dags_created', 'Number of successfully created DAGs')
dags_failed = Counter('dags_failed', 'Number of failed DAG creations')


def perform_crawl_task(site_profile: SiteProfileResponse, site_context: SiteContextResponse,
                       task_info: CrawlTaskResponse, **context):

    task_instance = context['ti']
    previous_result = task_instance.xcom_pull(key="processing_result", task_ids=task_instance.task_id)

    executor = TaskExecutor(
        site_profile=site_profile,
        site_context=site_context,
        task_info=task_info,
        previous_result=previous_result
    )

    result = asyncio.run(executor.execute())

    if task_info.type == "PROCESSING":
        task_instance.xcom_push(key="processing_result", value=str(result))

    return result


def generate_task_definitions(dag_id: str, site_profile: SiteProfileResponse, site_context: SiteContextResponse) -> list:

    return [
        {
            "task_id": f"{dag_id}_task_{task_info.step_order}",
            "operator": PythonOperator,
            "callable": perform_crawl_task,
            "op_kwargs": {
                "site_profile": site_profile,
                "site_context": site_context,
                "task_info": task_info,
            },
        }
        for endpoint in site_profile.crawl_endpoints
        for task_info in endpoint.crawl_tasks
    ]


def create_site_profile_dag(dag_id: str, schedule_interval: str, task_definitions: list) -> DAG:

    default_args = create_default_args()

    with DAG(dag_id=dag_id, default_args=default_args, schedule_interval=schedule_interval, catchup=False) as dag:
        previous_task = None

        for task_definition in task_definitions:
            task = task_definition["operator"](
                task_id=task_definition["task_id"],
                python_callable=task_definition["callable"],
                op_kwargs=task_definition["op_kwargs"],
                provide_context=True,
            )
            if previous_task:
                task.set_upstream(previous_task)
            previous_task = task

    return dag


def create_dags():

    config_dir = Path("/usr/src/app/dags/config")
    dags = []

    for config_file in config_dir.glob("crawl_config_site_*.yaml"):
        try:
            logging.info(f"Processing config file: {config_file}")
            site_context = SiteContextResponse.load_site_config(config_file)

            for site_profile in site_context.site_profiles:
                dag_id = f"crawl_site_{site_context.site_name}_{site_profile.mapping_id}"
                schedule_interval = f"*/{site_profile.crawl_setting.crawl_frequency} * * * *"

                task_definitions = generate_task_definitions(dag_id, site_profile, site_context)

                dag = create_site_profile_dag(dag_id, schedule_interval, task_definitions)
                globals()[dag_id] = dag
                dags_created.inc()
                logging.info(f"Successfully created DAG: {dag_id}")
                dags.append(dag)

        except Exception as e:
            dags_failed.inc()
            logging.error(f"Failed to create DAG from config file {config_file}: {e}")

    return dags


for dag in create_dags():
    globals()[dag.dag_id] = dag
