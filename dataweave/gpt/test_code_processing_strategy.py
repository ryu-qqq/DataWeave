import logging
from typing import List

from injector import inject, singleton

from dataweave.cache.test_code_cache_manager import TestCodeCacheManager
from dataweave.enums.batch_status import BatchStatus
from dataweave.gitlab.git_lab_client import GitLabClient
from dataweave.gpt.batch_models import Batch
from dataweave.gpt.batch_processing_strategy import BatchProcessingStrategy
from dataweave.gpt.models.processed_batch_data import ProcessedBatchData


@singleton
class TestCodeProcessingStrategy(BatchProcessingStrategy):

    @inject
    def __init__(self, git_lab_client: GitLabClient, test_code_cache_manager: TestCodeCacheManager):
        self.git_lab_client = git_lab_client
        self.test_code_cache_manager = test_code_cache_manager

    async def process_batch(self, batch: Batch, save_path: str) -> List[ProcessedBatchData]:
        processed_files = []
        changed_files = self._get_changed_files(batch)

        for file in changed_files:
            processed_data = await self._process_single_method(batch, file)
            processed_files.append(processed_data)

        return processed_files

    def _get_changed_files(self, batch: Batch) -> List[dict]:
        changed_files = batch.task_metadata.get("changed_files", [])
        if not changed_files:
            raise ValueError("No changed files found in batch metadata.")
        return changed_files

    async def _process_single_method(self, batch: Batch, method: dict) -> ProcessedBatchData:
        commit_id = batch.task_metadata["commit_id"]
        class_name = method["class_name"]
        method_name = method["method_name"]

        test_code = method.get("test_code")
        await self.test_code_cache_manager.update_method_status(
            commit_id=commit_id,
            class_name=class_name,
            method_name=method_name,
            status=BatchStatus.COMPLETED,
            test_code=test_code
        )

        return ProcessedBatchData(
            batch_id=batch.batch_id,
            data_type="test_code",
            content={"file_path": method["file_path"], "test_code": test_code},
            object_name=f"batch/test_code/{batch.batch_id}/{method['file_path']}_test.json",
        )




    def _get_base_branch(self, batch: Batch) -> str:
        return batch.task_metadata.get("base_branch", "main")

    async def _process_single_file(self, batch: Batch, file: dict, base_branch: str) -> ProcessedBatchData:
        branch_name = self._generate_branch_name(base_branch, file["file_path"])
        test_code = file.get("test_code")

        await self._git_push(batch, test_code, branch_name)
        await self._merge_request(batch, file, branch_name, base_branch)

        return ProcessedBatchData(
            batch_id=batch.batch_id,
            data_type="test_code",
            content={"file_path": file["file_path"], "test_code": test_code},
            object_name=f"batch/test_code/{batch.batch_id}/{file['file_path']}_test.json",
        )

    async def _git_push(self, batch: Batch, file: dict, branch_name: str):
        test_code = file.get("test_code")
        commit_message = f"Add test for {file['file_path']}"

        await self.git_lab_client.push_file(
            project_id=batch.task_metadata["project_id"],
            file_path=f"{file['file_path']}_test.java",
            branch=branch_name,
            content=test_code,
            commit_message=commit_message
        )

    async def _merge_request(self, batch: Batch, file: dict, branch_name: str, base_branch: str):
        await self.git_lab_client.create_merge_request(
            project_id=batch.task_metadata["project_id"],
            source_branch=branch_name,
            target_branch=base_branch,
            title=f"Test for {file['file_path']}"
        )

    def _generate_branch_name(self, base_branch: str, file_path: str) -> str:
        return f"{base_branch}-{hash(file_path)}"
