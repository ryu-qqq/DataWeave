import logging
import os
import requests
from airflow.models import Variable
from prometheus_client import Counter, Histogram

task_success = Counter('airflow_task_success', 'Count of successful tasks', ['dag_id', 'task_id'])
task_failure = Counter('airflow_task_failure', 'Count of failed tasks', ['dag_id', 'task_id'])
task_duration = Histogram('airflow_task_duration', 'Duration of task execution in seconds', ['dag_id', 'task_id'])


def send_slack_alert(context):
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
            f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}"
        )


def global_on_success_callback(context):
    task_id = context['task_instance'].task_id
    dag_id = context['dag'].dag_id
    task_success.labels(dag_id=dag_id, task_id=task_id).inc()
    task_duration.labels(dag_id=dag_id, task_id=task_id).observe(context['task_instance'].duration)


def global_on_failure_callback(context):
    task_id = context['task_instance'].task_id
    dag_id = context['dag'].dag_id
    task_failure.labels(dag_id=dag_id, task_id=task_id).inc()

    try:
        send_slack_alert(context)
    except Exception as e:
        logging.error(f"Failed to send Slack alert: {str(e)}")
