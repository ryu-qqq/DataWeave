import logging
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator

from dags.default_args import default_args
from dataweave.api_client.models.crawl_task_reponse import CrawlTaskResponse
from dataweave.api_client.models.site_context_response import SiteContextResponse
from dataweave.api_client.models.site_profile_reponse import SiteProfileResponse
from dataweave.coroutine_utils import CoroutineUtils
from dataweave.task_executor import TaskExecutor


def fetch_previous_result(task_instance, task_id: str):
    return task_instance.xcom_pull(task_ids=task_id)


def perform_crawl_task(site_profile: SiteProfileResponse, site_context: SiteContextResponse, task_info: CrawlTaskResponse, **context):
    task_instance = context['ti']
    previous_result = fetch_previous_result(task_instance, task_instance.task_id)

    executor = TaskExecutor(
        site_profile=site_profile,
        site_context=site_context,
        task_info=task_info,
        previous_result=previous_result
    )

    result = CoroutineUtils.run_async(executor.execute())

    if task_info.type == "PROCESSING":
        task_instance.xcom_push(key="processing_result", value=result)
    return result


def create_site_profile_dag(dag_id: str, site_context: SiteContextResponse, site_profile: SiteProfileResponse) -> DAG:
    schedule_interval = f"*/{site_profile.crawl_setting.crawl_frequency} * * * *"

    with DAG(dag_id=dag_id, default_args=default_args(), schedule_interval=schedule_interval, catchup=False) as dag:
        previous_task_id = None
        for endpoint in site_profile.crawl_endpoints:
            for task_info in endpoint.crawl_tasks:
                task_id = f"{dag_id}_endpoint_{endpoint.endpoint_id}_task_{task_info.step_order}"

                task = PythonOperator(
                    task_id=task_id,
                    python_callable=perform_crawl_task,
                    op_kwargs={
                        'site_profile': site_profile,
                        'site_context': site_context,
                        'task_info': task_info
                    },
                    provide_context=True
                )

                if previous_task_id and task_info.type == "PROCESSING":
                    task.set_upstream(previous_task_id)

                previous_task_id = task_id if task_info.type == "PROCESSING" else previous_task_id
    return dag


def create_dags():
    config_dir = Path("/usr/src/app/dags/config")
    dags = []
    logging.info(f"Checking config directory: {config_dir}")
    for config_file in config_dir.glob("crawl_config_site_*.yaml"):
        logging.info(f"Processing config file: {config_file}")
        try:
            site_context = SiteContextResponse.load_site_config(config_file)
            for site_profile in site_context.site_profiles:
                dag_id = f"crawl_site_{site_context.site_name}_{site_profile.mapping_id}"
                dag = create_site_profile_dag(dag_id, site_context, site_profile)
                globals()[dag_id] = dag
                logging.info(f"Created DAG with ID: {dag_id}")
                dags.append(dag)
        except Exception as e:
            logging.error(f"Error while creating DAG from {config_file}: {e}")
    return dags


for dag in create_dags():
    globals()[dag.dag_id] = dag
