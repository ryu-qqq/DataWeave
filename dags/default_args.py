from datetime import datetime
from airflow.settings import tz

from dags.slack_notify import slack_failed_task_alert


def default_args():
    return create_default_args()


def create_default_args(
        owner='ryuqq',
        depends_on_past=False,
        start_date=None,
        retries=1,
        email_on_failure=False,
        email_on_retry=False,
        retry_delay=None,
        on_failure_callback=slack_failed_task_alert
):
    """
    default_args를 동적으로 생성하는 함수
    :param on_failure_callback: slack notification callback
    :param owner: DAG의 소유자 (기본값: 'airflow')
    :param depends_on_past: 이전 실행에 의존 여부 (기본값: False)
    :param retries: 재시도 횟수 (기본값: 1)
    :param email_on_failure: 실패 시 이메일 알림 (기본값: False)
    :param email_on_retry: 재시도 시 이메일 알림 (기본값: False)
    :param retry_delay: 재시도 딜레이 (기본값: None)
    :return: 생성된 default_args 딕셔너리
    """
    default_args = {
        'owner': owner,
        'depends_on_past': depends_on_past,
        'start_date': start_date or datetime(2024, 11, 5),
        'retries': retries,
        'email_on_failure': email_on_failure,
        'email_on_retry': email_on_retry,
        'on_failure_callback': on_failure_callback,
    }

    if retry_delay:
        default_args['retry_delay'] = retry_delay

    return default_args
