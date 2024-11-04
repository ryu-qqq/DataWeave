from datetime import datetime, timedelta

def create_default_args(
        owner='ryuqq',
        depends_on_past=False,
        start_date_offset_minutes=1,
        retries=1,
        email_on_failure=False,
        email_on_retry=False,
        retry_delay=None
):
    """
    default_args를 동적으로 생성하는 함수
    :param owner: DAG의 소유자 (기본값: 'airflow')
    :param depends_on_past: 이전 실행에 의존 여부 (기본값: False)
    :param start_date_offset_minutes: 시작 날짜의 오프셋 (현재 시간 기준, 기본값: 1분 전)
    :param retries: 재시도 횟수 (기본값: 1)
    :param email_on_failure: 실패 시 이메일 알림 (기본값: False)
    :param email_on_retry: 재시도 시 이메일 알림 (기본값: False)
    :param retry_delay: 재시도 딜레이 (기본값: None)
    :return: 생성된 default_args 딕셔너리
    """
    default_args = {
        'owner': owner,
        'depends_on_past': depends_on_past,
        'start_date': datetime.now() - timedelta(minutes=start_date_offset_minutes),
        'retries': retries,
        'email_on_failure': email_on_failure,
        'email_on_retry': email_on_retry,
    }

    if retry_delay:
        default_args['retry_delay'] = retry_delay

    return default_args
