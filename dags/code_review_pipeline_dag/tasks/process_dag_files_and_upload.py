import asyncio
import logging
import os

from airflow.models import Variable

from modules.aws.s3_service import s3_service


async def upload_files_to_s3_and_cleanup(base_dir: str, s3_prefix: str):
    try:
        files_uploaded = []
        for root, _, files in os.walk(base_dir):
            for file_name in files:
                local_file_path = os.path.join(root, file_name)
                s3_object_name = f"{s3_prefix}/{file_name}"

                await s3_service.upload_json_data(open(local_file_path, 'r').read(), s3_object_name)

                os.remove(local_file_path)
                logging.info(f"Uploaded and deleted file: {local_file_path}")

                files_uploaded.append({
                    "local_path": local_file_path,
                    "s3_path": f"s3://{s3_service.aws_client.bucket_name}/{s3_object_name}"
                })

        return files_uploaded
    except Exception as e:
        logging.error(f"Error uploading files to S3: {e}")
        raise


def process_dag_files_and_upload(**kwargs):
    ti = kwargs["ti"]

    review_dir = Variable.get("REVIEW_RESULT_DIR", "/tmp/airflow_files/reviews/result")
    test_dir = Variable.get("TEST_RESULT_DIR", "/tmp/airflow_files/test/result")
    s3_prefix = f"{Variable.get('dag_id', 'airflow_dag')}/{Variable.get('execution_date', 'unknown')}"

    loop = asyncio.get_event_loop()
    review_files = loop.run_until_complete(upload_files_to_s3_and_cleanup(review_dir, f"{s3_prefix}/reviews"))
    test_files = loop.run_until_complete(upload_files_to_s3_and_cleanup(test_dir, f"{s3_prefix}/tests"))

    ti.xcom_push(key="uploaded_files", value={"reviews": review_files, "tests": test_files})
