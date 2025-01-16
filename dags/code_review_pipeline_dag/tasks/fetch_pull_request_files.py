import asyncio
from typing import Dict

from modules.spring_core_server.git.git_fetcher import spring_git_fetcher


async def fetch_files_for_pr(pull_request_id: int, git_type: str) -> Dict:
    files = await spring_git_fetcher.fetch_pull_request_files(pull_request_id)
    return {
        "pull_request_id": pull_request_id,
        "git_type": git_type,
        "files": [file.to_dict() for file in files],
    }


async def fetch_pull_request_files_async(**kwargs) -> Dict:
    try:
        pull_request_data = kwargs["ti"].xcom_pull(task_ids="fetch_pull_requests")

        if not pull_request_data or not pull_request_data.get("content"):
            return {"files": [], "message": "No Pull Request files to fetch."}

        pull_request_ids_and_types = [
            {"id": pr["id"], "git_type": pr["git_type"]}
            for pr in pull_request_data["content"]
        ]

        tasks = [
            fetch_files_for_pr(pr["id"], pr["git_type"])
            for pr in pull_request_ids_and_types
        ]
        results = await asyncio.gather(*tasks)

        return {"pull_requests": results}

    except Exception as e:
        raise RuntimeError(f"Failed to fetch pull request files: {e}")


def fetch_pull_request_files(**kwargs) -> Dict:
    return asyncio.run(fetch_pull_request_files_async(**kwargs))
