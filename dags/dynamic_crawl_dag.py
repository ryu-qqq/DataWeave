import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

from dataweave.api_client.models.crawl_auth_setting_response import CrawlAuthSettingResponse
from dataweave.api_client.models.crawl_task_reponse import CrawlTaskResponse
from dataweave.api_client.models.site_profile_reponse import SiteProfileResponse
from dataweave.api_client.product_hub_api_client import product_hub_api_client
from dataweave.coroutine_utils import CoroutineUtils
from dataweave.crawl_task_executor_service import CrawlTaskExecutorService
from dataweave.crawl_task_request import CrawlTaskRequest
from dataweave.enums.task_type import TaskType
from default_args import create_default_args


def create_crawl_task(site_name: str, crawl_type: str, base_url: str, end_point_url: str, parameters: str,
                    auth_settings: CrawlAuthSettingResponse, task: CrawlTaskResponse, headers, **context):

    previous_result = None
    if task.task_type == TaskType.X_COM.name:
        previous_result = context['ti'].xcom_pull(task_ids=context.get('prev_task_id'))

    logging.info(f"Executing task: {task.task_type} on endpoint ID {task.endpoint_id}")

    crawl_task_request = CrawlTaskRequest(
        site_name=site_name,
        crawl_type=crawl_type,
        base_url=base_url,
        end_point_url=end_point_url,
        parameters=parameters,
        task=task,
        headers=headers,
        auth_settings=auth_settings,
        previous_result=previous_result
    )

    result_data = CoroutineUtils.run_async(CrawlTaskExecutorService.do_task(crawl_task_request))
    return result_data


def create_site_profile_dag(site_name: str, base_url: str, site_profile: SiteProfileResponse):
    dag_id = f"crawl_site_{site_name}_{site_profile.mapping_id}"

    crawl_frequency = site_profile.crawl_setting.crawl_frequency
    schedule_interval = f"*/{crawl_frequency} * * * *"
    crawl_type = site_profile.crawl_setting.crawl_type

    auth_settings = site_profile.crawl_auth_setting

    with DAG(dag_id=dag_id,
             default_args=create_default_args(),
             catchup=False,
             schedule_interval=schedule_interval) as dag:

        for endpoint in site_profile.crawl_endpoints:
            with TaskGroup(group_id=f"endpoint_{site_profile.mapping_id}_{endpoint.endpoint_id}") as endpoint_group:
                previous_task_id = None

                for task_data in endpoint.crawl_tasks:
                    crawl_task = PythonOperator(
                        task_id=f"crawl_task_{task_data.endpoint_id}_step_{task_data.step_order}",
                        python_callable=create_crawl_task,
                        op_kwargs={
                            'site_name': site_name,
                            'crawl_type': crawl_type,
                            'base_url': base_url,
                            'end_point_url': endpoint.end_point_url,
                            'parameters': endpoint.parameters,
                            'task': task_data,
                            'auth_settings': auth_settings,
                            'headers': site_profile.headers
                        },
                        provide_context=True
                    )

                    if previous_task_id:
                        crawl_task.op_kwargs['prev_task_id'] = previous_task_id

                    previous_task_id = crawl_task.task_id

    return dag


def create_dags():
    sites = product_hub_api_client.fetch_sites()
    for site in sites.content:
        site_context = product_hub_api_client.fetch_site_context(site.site_id)
        site_name = site_context.site_name
        base_url = site_context.base_url
        for site_profile in site_context.site_profiles:
            globals()[f"crawl_site_{site_context.site_name}_{site_profile.mapping_id}"] = create_site_profile_dag(
                site_name,
                base_url,
                site_profile)


create_dags()
