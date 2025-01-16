import json
import logging
from typing import Dict

from modules.generate_ai.models.code import Code
from modules.generate_ai.models.open_ai_enums import CodeType, GenerativeAiType
from modules.generate_ai.reviewer.review_provider import reviewer_provider


def load_file_content(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_data = json.load(file)
            return file_data.get("content", "")
    except Exception as e:
        logging.error(f"Failed to load file content from {file_path}: {e}")
        return ""


def review_pull_request_code(**kwargs) -> Dict:
    try:
        ti = kwargs["ti"]
        saved_files = ti.xcom_pull(task_ids="fetch_pull_request_file_contents")

        if not saved_files or not saved_files.get("files"):
            logging.warning("No files found to review.")
            return {"reviews": [], "summary": {"total_files": 0, "successful": 0, "failed": 0}}

        review_results = []
        failed_reviews = 0

        for file_metadata in saved_files["files"]:
            local_path = file_metadata.get("localPath")
            if not local_path:
                logging.warning(f"No local path found for file: {file_metadata['filePath']}")
                failed_reviews += 1
                review_results.append({
                    **file_metadata,
                    "review": None,
                    "status": "failed",
                    "error": "Local path not found"
                })
                continue

            content = load_file_content(local_path)
            if not content:
                logging.warning(f"Empty content for file: {file_metadata['filePath']}")
                failed_reviews += 1
                review_results.append({
                    **file_metadata,
                    "review": None,
                    "status": "failed",
                    "error": "File content is empty"
                })
                continue

            code = Code(
                code_type=CodeType.JAVA,
                ai_type=GenerativeAiType.OPENAI,
                source=content
            )

            reviewer = reviewer_provider.get_reviewer(code)
            if not reviewer:
                logging.warning(f"No reviewer found for file: {file_metadata['filePath']}")
                failed_reviews += 1
                review_results.append({
                    **file_metadata,
                    "review": None,
                    "status": "failed",
                    "error": "Reviewer not found"
                })
                continue

            try:
                review_result = reviewer.review_code(code)
                review_results.append({
                    **file_metadata,
                    "review": review_result,
                    "status": "success"
                })
            except Exception as review_error:
                logging.error(f"Error during review for file {file_metadata['filePath']}: {review_error}")
                failed_reviews += 1
                review_results.append({
                    **file_metadata,
                    "review": None,
                    "status": "failed",
                    "error": str(review_error)
                })

        total_files = len(saved_files["files"])
        successful_reviews = total_files - failed_reviews

        summary = {
            "total_files": total_files,
            "successful": successful_reviews,
            "failed": failed_reviews
        }
        logging.info(f"Review summary: {summary}")

        return {"reviews": review_results, "summary": summary}

    except Exception as e:
        logging.error(f"Failed to review pull request code: {e}")
        raise RuntimeError(f"Failed to review pull request code: {e}")
