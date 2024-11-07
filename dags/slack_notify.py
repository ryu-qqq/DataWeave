import os
import requests
from airflow.models import Variable


def slack_failed_task_alert(context):
    slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL") or Variable.get("slack_webhook_url")
    task_instance = context.get('task_instance')
    dag_id = task_instance.dag_id
    task_id = task_instance.task_id
    execution_date = context.get('execution_date')
    log_url = task_instance.log_url

    message = {
        "text": f":red_circle: Task Failed!\n*DAG*: {dag_id}\n*Task*: {task_id}\n*Execution Time*: {execution_date}\n<{log_url}|See Logs>"
    }

    response = requests.post(slack_webhook_url, json=message)
    if response.status_code != 200:
        raise ValueError(
            f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")
