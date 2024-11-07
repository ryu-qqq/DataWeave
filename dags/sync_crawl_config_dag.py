from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator

from dags.default_args import default_args
from dataweave.api_client.product_hub_api_client import product_hub_api_client
from dataweave.crawl_config_saver import CrawlConfigSaver


def fetch_and_save_config():
    sites = product_hub_api_client.fetch_sites(site_type="CRAWL")

    for site in sites.content:
        site_context = product_hub_api_client.fetch_site_context(site.site_id)
        file_path = Path("/usr/src/app/dags/config") / f'crawl_config_site_{site_context.site_id}.yaml'
        file_path.parent.mkdir(parents=True, exist_ok=True)
        CrawlConfigSaver.save_to_yaml(site_context, file_path)


with DAG(
        dag_id="sync_crawl_config",
        default_args=default_args(),
        schedule_interval="0 * * * *",
        catchup=False,
) as dag:
    fetch_config_task = PythonOperator(
        task_id="fetch_and_save_config",
        python_callable=fetch_and_save_config,
    )
