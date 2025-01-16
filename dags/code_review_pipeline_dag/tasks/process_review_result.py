import logging

from airflow.models import Variable
from modules.generate_ai.models.code_review_report import CodeReviewReport
import os

from modules.utils.file_manager import FileManager


def process_review_result(**kwargs):
    try:
        ti = kwargs["ti"]
        review_results = ti.xcom_pull(task_ids="code_review_task")

        if not review_results or not review_results.get("reviews"):
            raise ValueError("No review results found.")

        base_dir = Variable.get("REVIEW_RESULT_DIR", "/tmp/airflow_files/reviews/result")
        os.makedirs(base_dir, exist_ok=True)

        processed_results = {
            "successful_reviews": [],
            "failed_reviews": [],
            "summary": {
                "total_reviews": len(review_results["reviews"]),
                "successful": 0,
                "failed": 0
            }
        }

        for review_data in review_results["reviews"]:
            file_path = review_data["filePath"]
            review_result_data = review_data.get("review")
            review_result = {}
            if review_result_data:
                review_result = CodeReviewReport(**review_result_data)
                review_status = "success"
            else:
                review_status = "failed"

            review_file_name = f"{os.path.basename(file_path)}_review.json"
            review_file_path = os.path.join(base_dir, review_file_name)

            if review_status == "success":
                with open(review_file_path, "w", encoding="utf-8") as f:
                    f.write(review_result.to_json())
                logging.info(f"Review result saved: {review_file_path}")

                processed_results["successful_reviews"].append({
                    "owner": review_data["owner"],
                    "repository": review_data["repositoryName"],
                    "filePath": review_data["filePath"],
                    "git_type": review_data["git_type"],
                    "review_file_path": review_file_path
                })

                processed_results["summary"]["successful"] += 1

                if not review_result.test_required:
                    local_path = review_data.get("localPath")
                    if local_path:
                        FileManager.cleanup_downloaded_file(local_path)
                        logging.info(f"Deleted source code file: {local_path}")

            else:
                processed_results["failed_reviews"].append({
                    "owner": review_data["owner"],
                    "repository": review_data["repositoryName"],
                    "filePath": review_data["filePath"],
                    "git_type": review_data["git_type"],
                    "error": review_data.get("error")
                })
                processed_results["summary"]["failed"] += 1

        logging.info(f"Processed review summary: {processed_results['summary']}")
        ti.xcom_push(key="processed_review_results", value=processed_results)

    except Exception as e:
        logging.error(f"Failed to process review results: {e}")
        raise RuntimeError(f"Failed to process review results: {e}")