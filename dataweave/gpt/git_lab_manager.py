import requests
import logging
from injector import singleton, inject


@singleton
class GitLabManager:

    @inject
    def __init__(self):
        self.__headers = {"PRIVATE-TOKEN": "glpat-tJsjePB-EPx-CZnJUVxr"}

    def check_file_exists(self, project_id: int, branch_name: str, file_path: str) -> bool:

        file_url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/files/{file_path.replace('/', '%2F')}"
        params = {"ref": branch_name}
        file_response = requests.get(file_url, headers=self.__headers, params=params)

        if file_response.status_code == 200:
            return True
        elif file_response.status_code == 404:
            return False
        else:
            raise ValueError(f"Failed to check file existence: {file_response.content}")

    def create_commit_data(self, branch_name: str, file_path: str, file_content: str, commit_message: str,
                           action: str) -> dict:
        return {
            "branch": branch_name,
            "commit_message": commit_message,
            "actions": [
                {
                    "action": action,
                    "file_path": file_path,
                    "content": file_content,
                }
            ],
        }

    def push_commit(self, project_id: int, data: dict):
        url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/commits"
        response = requests.post(url, headers=self.__headers, json=data)

        if response.status_code != 201:
            raise ValueError(f"Failed to push to GitLab: {response.content}")

        logging.info(f"Successfully pushed commit to GitLab.")
        return response.json()

    def create_branch(self, project_id: int, new_branch_name: str, ref_branch: str):
        url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/branches"
        data = {"branch": new_branch_name, "ref": ref_branch}
        response = requests.post(url, headers=self.__headers, json=data)

        if response.status_code != 201:
            raise ValueError(f"Failed to create branch: {response.content}")

        logging.info(f"Branch '{new_branch_name}' created successfully.")

    def push_to_gitlab(self, project_id: int, branch_name: str, class_name: str, file_path: str, file_content: str,
                       commit_message: str):

        try:
            sanitized_branch_name = branch_name.replace("refs/heads/", "")
            new_branch_name = f"{sanitized_branch_name}_{class_name}_auto"

            try:
                self.create_branch(project_id, new_branch_name, sanitized_branch_name)
            except ValueError as e:
                if "already exists" in str(e):
                    logging.info(f"Branch '{new_branch_name}' already exists.")
                else:
                    raise

            file_exists = self.check_file_exists(project_id, new_branch_name, file_path)
            action = "update" if file_exists else "create"

            commit_data = self.create_commit_data(new_branch_name, file_path, file_content, commit_message, action)
            return self.push_commit(project_id, commit_data)

        except Exception as e:
            logging.error(f"Error pushing to GitLab: {e}")
            raise
