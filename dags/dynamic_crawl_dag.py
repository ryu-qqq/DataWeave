import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from default_args import create_default_args

from dataweave.api_client.models.crawl_task_reponse import CrawlTaskResponse
from dataweave.api_client.product_hub_api_client import product_hub_api_client
from dataweave.crawler.auth.auth_provider_factory import AuthProviderFactory


def create_crawl_task(crawl_type: str, end_point_url: str, parameters: str, task: CrawlTaskResponse, headers, **kwargs):
    logging.info(f"Executing task: {task.task_type} on endpoint ID {task.endpoint_id}")
    logging.info(f"Using headers: {headers}")


def create_site_profile_dag(site_name: str, site_profile):
    dag_id = f"crawl_site_{site_name}_{site_profile.mapping_id}"

    crawl_frequency = site_profile.crawl_setting.crawl_frequency
    schedule_interval = f"*/{crawl_frequency} * * * *"
    crawl_type = site_profile.crawl_setting.crawl_type

    auth_settings = site_profile.crawl_auth_setting

    with DAG(dag_id=dag_id,
             default_args=create_default_args(),
             schedule_interval=schedule_interval) as dag:

        auth_provider = AuthProviderFactory.get_auth_provider(auth_settings.auth_type)
        headers = auth_provider.authenticate(
            auth_endpoint=auth_settings.auth_endpoint,
            headers=site_profile.headers,
            auth_header=auth_settings.auth_headers,
            payload=auth_settings.auth_payload
        )

        for endpoint in site_profile.crawl_endpoints:
            with TaskGroup(group_id=f"endpoint_{site_profile.mapping_id}_{endpoint.endpoint_id}") as endpoint_group:
                for task_data in endpoint.crawl_tasks:
                    task = PythonOperator(
                        task_id=f"crawl_task_{task_data.endpoint_id}_step_{task_data.step_order}",
                        python_callable=create_crawl_task,
                        op_kwargs={
                            'crawl_type': crawl_type, 'end_point_url': endpoint.end_point_url,
                            'parameters': endpoint.parameters, 'task': task_data, 'headers': headers}
                    )

    return dag


def create_dags():
    sites = product_hub_api_client.fetch_sites()
    for site in sites.content:
        site_context = product_hub_api_client.fetch_site_context(site.site_id)
        site_name = site_context.site_name
        for site_profile in site_context.site_profiles:
            globals()[f"crawl_site_{site_context.site_name}_{site_profile.mapping_id}"] = create_site_profile_dag(site_name,
                site_profile)


create_dags()
