import logging
import os

from airflow.models import Variable

from modules.generate_ai.models.code import Code
from modules.generate_ai.models.test_review_report import TestCodeReport
from modules.generate_ai.tester.test_provider import tester_provider
from modules.generate_ai.models.open_ai_enums import CodeType, GenerativeAiType


def generate_tests_for_reviewed_files(**kwargs):
    try:
        ti = kwargs["ti"]
        detailed_review_results = ti.xcom_pull(task_ids="process_review_result")

        if not detailed_review_results or not detailed_review_results.get("successful_reviews"):
            raise ValueError("No detailed review results found.")

        base_dir = Variable.get("TEST_RESULT_DIR", "/tmp/airflow_files/test/result")
        os.makedirs(base_dir, exist_ok=True)

        test_results = {
            "successful_tests": [],
            "failed_tests": [],
            "summary": {
                "total_files": len(detailed_review_results["successful_reviews"]),
                "successful": 0,
                "failed": 0
            }
        }

        for review_data in detailed_review_results["successful_reviews"]:
            review = review_data.get("review")
            if not review or not review.get("test_required"):
                logging.info(f"No test required for file: {review_data['filePath']}")
                continue

            file_path = review_data["filePath"]
            suggested_code = review.get("suggested_code")

            if not suggested_code:
                logging.warning(f"No suggested code for file: {file_path}")
                test_results["failed_tests"].append({
                    "filePath": file_path,
                    "reason": "No suggested code provided"
                })
                test_results["summary"]["failed"] += 1
                continue

            code = Code(
                code_type=CodeType.JAVA,
                ai_type=GenerativeAiType.OPENAI,
                source=suggested_code
            )

            tester = tester_provider.get_reviewer(code)
            if not tester:
                logging.warning(f"No tester available for file: {file_path}")
                test_results["failed_tests"].append({
                    "filePath": file_path,
                    "reason": "No tester available"
                })
                test_results["summary"]["failed"] += 1
                continue

            try:
                test_report: TestCodeReport = tester.write_tests(code)

                test_file_name = f"{os.path.basename(file_path)}_test.json"
                test_file_path = os.path.join(base_dir, test_file_name)
                with open(test_file_path, "w", encoding="utf-8") as f:
                    f.write(test_report.to_json())
                logging.info(f"Test result saved: {test_file_path}")

                test_results["successful_tests"].append({
                    "owner": review_data["owner"],
                    "repository": review_data["repository"],
                    "filePath": file_path,
                    "git_type": review_data["git_type"],
                    "test_file_path": test_file_path
                })
                test_results["summary"]["successful"] += 1

            except Exception as e:
                logging.error(f"Error generating test for file {file_path}: {e}")
                test_results["failed_tests"].append({
                    "filePath": file_path,
                    "reason": str(e)
                })
                test_results["summary"]["failed"] += 1

        logging.info(f"Test results summary: {test_results['summary']}")
        ti.xcom_push(key="test_results", value=test_results)

    except Exception as e:
        logging.error(f"Failed to generate tests for reviewed files: {e}")
        raise RuntimeError(f"Failed to generate tests for reviewed files: {e}")