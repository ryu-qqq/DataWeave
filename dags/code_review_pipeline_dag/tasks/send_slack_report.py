import logging
import os

import requests
from airflow.models import Variable


def send_dag_report_to_slack(**kwargs):
    """Send DAG results as a report to Slack."""
    ti = kwargs["ti"]
    uploaded_files = ti.xcom_pull(task_ids="process_dag_files_and_upload", key="uploaded_files")

    if not uploaded_files:
        raise ValueError("No uploaded files found to report.")

    reviews = uploaded_files.get("reviews", [])
    tests = uploaded_files.get("tests", [])

    slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL") or Variable.get("slack_webhook_url")

    report_message = f"""
    *DAG Execution Report*
    Reviews Uploaded: {len(reviews)}
    Tests Uploaded: {len(tests)}

    S3 Links:
    Reviews: {', '.join([file['s3_path'] for file in reviews])}
    Tests: {', '.join([file['s3_path'] for file in tests])}
    """

    response = requests.post(slack_webhook_url, json={"text": report_message})
    if response.status_code != 200:
        raise ValueError(f"Slack API responded with {response.status_code}: {response.text}")

    logging.info("Slack report sent successfully.")