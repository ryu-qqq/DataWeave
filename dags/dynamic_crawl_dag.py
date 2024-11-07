import logging
from pathlib import Path
from typing import Dict
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from dags.default_args import default_args
from dataweave.api_client.models.crawl_auth_setting_response import CrawlAuthSettingResponse
from dataweave.api_client.models.crawl_endpoint_response import CrawlEndpointResponse
from dataweave.api_client.models.crawl_task_reponse import CrawlTaskResponse
from dataweave.api_client.models.site_context_response import SiteContextResponse
from dataweave.api_client.models.site_profile_reponse import SiteProfileResponse
from dataweave.coroutine_utils import CoroutineUtils
from dataweave.crawl_task_executor import CrawlTaskExecutor


def perform_crawl_task(
        crawl_type: str, headers: Dict[str, str],
        site_context: SiteContextResponse, auth_settings: CrawlAuthSettingResponse,
        crawl_end_point: CrawlEndpointResponse, task_info: CrawlTaskResponse, **context):
    CoroutineUtils.run_async(
        CrawlTaskExecutor.perform_crawling(
            crawl_type=crawl_type,
            headers=headers,
            site_context=site_context,
            auth_settings=auth_settings,
            crawl_end_point=crawl_end_point,
            task_info=task_info
        )
    )


def create_site_profile_dag(dag_id: str, site_context: SiteContextResponse, site_profile: SiteProfileResponse) -> DAG:
    schedule_interval = f"*/{site_profile.crawl_setting.crawl_frequency} * * * *"
    with DAG(dag_id=dag_id, default_args=default_args(), schedule_interval=schedule_interval, catchup=False) as dag:
        for endpoint in site_profile.crawl_endpoints:
            for task_info in endpoint.crawl_tasks:
                PythonOperator(
                    task_id=f"{dag_id}_endpoint_{endpoint.endpoint_id}_task_{task_info.step_order}",
                    python_callable=perform_crawl_task,
                    op_kwargs={
                        'crawl_type': site_profile.crawl_setting.crawl_type,
                        'headers': site_profile.headers,
                        'site_context': site_context,
                        'auth_settings': site_profile.crawl_auth_setting,
                        'crawl_end_point': endpoint,
                        'task_info': task_info
                    },
                    provide_context=True
                )
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
