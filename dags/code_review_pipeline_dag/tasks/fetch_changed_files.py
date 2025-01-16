import asyncio
import logging
import os
from typing import Dict, List

from modules.git_hub.git_hub_client import git_hub_client
from modules.utils.file_manager import FileManager


async def fetch_file_content(git_type: str, file_metadata: Dict) -> Dict:
    try:
        owner = file_metadata["owner"]
        repository_name = file_metadata["repositoryName"]
        file_path = file_metadata["filePath"]
        branch = "main"

        raw_content = await git_hub_client.get_file_content(owner, repository_name, file_path, branch)

        return {
            **file_metadata,
            "git_type": git_type,
            "rawContent": raw_content,
            "status": "success"
        }
    except Exception as e:
        logging.error(f"Error fetching content for {file_metadata['filePath']}: {e}")
        return {
            **file_metadata,
            "git_type": git_type,
            "rawContent": None,
            "status": "error",
            "error": str(e)
        }


async def save_file_content(file_metadata: Dict, base_directory: str) -> Dict:
    try:
        file_name = file_metadata["filePath"].replace("/", "_") + ".json"
        save_path = os.path.join(base_directory, file_name)

        if file_metadata.get("rawContent"):
            await FileManager.save_json_to_file(
                {
                    "owner": file_metadata["owner"],
                    "repository": file_metadata["repositoryName"],
                    "filePath": file_metadata["filePath"],
                    "git_type": file_metadata["git_type"],
                    "content": file_metadata["rawContent"]
                },
                save_path
            )
            logging.info(f"File saved: {save_path}")
            return {**file_metadata, "localPath": save_path, "status": "saved"}
        else:
            logging.warning(f"No content to save for file: {file_metadata['filePath']}")
            return {**file_metadata, "localPath": None, "status": "no_content"}

    except Exception as e:
        logging.error(f"Failed to save file content: {e}")
        return {**file_metadata, "localPath": None, "status": "error", "error": str(e)}


async def fetch_and_save_files(all_files_metadata: List[Dict], base_directory: str, git_type: str) -> List[Dict]:
    fetch_tasks = [fetch_file_content(git_type, file_metadata) for file_metadata in all_files_metadata]
    fetched_files = await asyncio.gather(*fetch_tasks)

    save_tasks = [save_file_content(file_metadata, base_directory) for file_metadata in fetched_files]
    return await asyncio.gather(*save_tasks)


async def fetch_pull_request_file_contents_async(**kwargs) -> Dict:
    try:
        ti = kwargs["ti"]
        pull_request_files = ti.xcom_pull(task_ids="fetch_pull_request_files")

        if not pull_request_files or not pull_request_files.get("pull_requests"):
            logging.warning("No pull request files found.")
            return {"files": [], "message": "No files to fetch content for."}

        all_files_metadata = [
            file for pr_data in pull_request_files["pull_requests"] for file in pr_data["files"]
        ]

        pull_request_id = pull_request_files["pull_requests"]["pull_request_id"]
        git_type = pull_request_files["pull_requests"]["git_type"]

        base_directory = f"/tmp/airflow_files/reviews/{pull_request_id}"
        os.makedirs(base_directory, exist_ok=True)

        saved_files = await fetch_and_save_files(all_files_metadata, base_directory, git_type)

        successful_files = [file for file in saved_files if file["status"] == "saved"]
        failed_files = [file for file in saved_files if file["status"] != "saved"]

        summary = {
            "files": saved_files,
            "summary": {
                "total_files": len(saved_files),
                "successful": len(successful_files),
                "failed": len(failed_files)
            }
        }
        logging.info(f"Fetch and save summary: {summary['summary']}")
        return summary

    except Exception as e:
        logging.error(f"Failed to fetch and save file contents: {e}")
        raise RuntimeError(f"Failed to fetch and save file contents: {e}")


def fetch_pull_request_file_contents(**kwargs) -> Dict:
    return asyncio.run(fetch_pull_request_file_contents_async(**kwargs))
