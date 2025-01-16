import logging
from airflow.providers.jenkins.operators.jenkins_job_trigger import JenkinsJobTriggerOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.models import Variable


def trigger_jenkins_job(**kwargs):
    """
    Trigger a Jenkins job to execute JaCoCo and upload the report to S3.
    """
    try:
        jenkins_job_name = Variable.get("JENKINS_JOB_NAME", "JACOCO_TEST_JOB")
        jenkins_params = {
            "ref": kwargs.get("params", {}).get("ref", "refs/heads/main")
        }

        trigger = JenkinsJobTriggerOperator(
            task_id="trigger_jenkins_job",
            jenkins_connection_id="jenkins_default",
            job_name=jenkins_job_name,
            parameters=jenkins_params
        )
        trigger.execute(context=kwargs)

        logging.info(f"Jenkins job {jenkins_job_name} triggered successfully.")
    except Exception as e:
        logging.error(f"Failed to trigger Jenkins job: {e}")
        raise RuntimeError(f"Failed to trigger Jenkins job: {e}")


def fetch_jenkins_job_status(**kwargs):
    """
    Fetch the status of the triggered Jenkins job and return the report link.
    """
    try:
        # Jenkins job details
        jenkins_job_name = Variable.get("JENKINS_JOB_NAME", "JACOCO_TEST_JOB")
        jenkins_report_path = Variable.get("JENKINS_REPORT_PATH", "s3://my-bucket/jacoco-reports/index.html")

        status_sensor = HttpSensor(
            task_id="check_jenkins_status",
            http_conn_id="jenkins_default",
            endpoint=f"/job/{jenkins_job_name}/lastBuild/api/json",
            response_check=lambda response: response.json().get("building") is False,
            poke_interval=30,
            timeout=600
        )
        status_sensor.execute(context=kwargs)

        logging.info(f"Jenkins job {jenkins_job_name} completed successfully.")
        return {"report_link": jenkins_report_path}
    except Exception as e:
        logging.error(f"Failed to fetch Jenkins job status: {e}")
        raise RuntimeError(f"Failed to fetch Jenkins job status: {e}")