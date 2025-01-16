import asyncio
import json
import logging
import os
from typing import List, Optional

from injector import singleton, inject, Injector

from modules.open_ai.openai_client import OpenAIClient
from modules.gpt.models.batch_status import BatchStatus
from modules.gpt.batch_id_manager import BatchIdManager
from modules.gpt.git_lab_manager import GitLabManager
from modules.gpt.models.batch_models import Batch
from modules.gpt.models.prompt_models import TestCodeMetadata
from modules.gpt.openai_response_handler import OpenAIResponseHandler
from modules.gpt.test_code_enhancer_prompt_generator import TestCodeEnhancerPromptGenerator


@singleton
class TestCodeEnhancer:

    @inject
    def __init__(self,
                 batch_id_manager: BatchIdManager,
                 open_ai_client: OpenAIClient,
                 test_code_enhancer_prompt_generator: TestCodeEnhancerPromptGenerator,
                 response_handler: OpenAIResponseHandler,
                 gitlab_push_manager: GitLabManager
                 ):
        self.__batch_id_manager = batch_id_manager
        self.__openai_client = open_ai_client
        self.__test_code_enhancer_prompt_generator = test_code_enhancer_prompt_generator
        self.__response_handler = response_handler
        self.__gitlab_manager = gitlab_push_manager
        self.__base_dir = os.path.join(os.getcwd(), "batch", "enhanced")
        os.makedirs(self.__base_dir, exist_ok=True)

    async def enhance(self):
        logging.info("Fetching ENHANCED batches...")
        batches: List[Batch[TestCodeMetadata]] = await self.__batch_id_manager.list_batches_by_status(
            BatchStatus.ENHANCED)
        if not batches:
            logging.info("No ENHANCED batches found.")
            return

        for batch in batches:
            try:
                save_path = self.__get_save_path(batch.batch_id)
                await self.__download_batch_results(batch, save_path)

                with open(save_path, "r") as file:
                    raw_data = json.load(file)

                response = self.__process_with_openai(batch, raw_data)
                enhanced_code = self.__response_handler.extract_enhanced_code_from_string(response)

                self.__push_to_gitlab(batch, enhanced_code)
                await self.__update_batch_status(batch, BatchStatus.READY_FOR_REVIEW)

            except Exception as e:
                logging.error(f"Error processing batch {batch.batch_id}: {e}")
                await self.__update_batch_status(batch, BatchStatus.FAILED)

    def __process_with_openai(self, batch: Batch, raw_data: dict) -> str:
        try:
            prompt = self.__test_code_enhancer_prompt_generator.get_prompt(raw_data)

            return self.__openai_client.generate_prompt(
                system_message=prompt.system_message,
                user_message=prompt.user_message,
                model="gpt-4o",
                temperature=0.5,
            )

        except Exception as e:
            logging.error(f"Error enhancing batch {batch.batch_id}: {e}")
            raise

    def __push_to_gitlab(self, batch: Batch[TestCodeMetadata], enhanced_code: str):
        project_id = batch.metadata.project_id
        branch_name = batch.metadata.branch_name
        class_name = batch.metadata.class_name
        file_path = batch.metadata.file_path
        commit_message = f"Enhanced test code for batch {batch.batch_id} By Open Ai"

        self.__gitlab_manager.push_to_gitlab(
            project_id, branch_name, class_name, file_path, enhanced_code, commit_message
        )

    async def __update_batch_status(self, batch: Batch, new_status: BatchStatus, enhanced_s3_url: Optional[str] = None):
        previous_status = batch.status
        batch.update_status(new_status)
        if enhanced_s3_url:
            batch.update_s3_url(enhanced_s3_url)
        await self.__batch_id_manager.update_batch(batch)
        logging.info(f"Batch {batch.batch_id} status updated: {previous_status} -> {new_status}")

    async def __download_batch_results(self, batch: Batch, save_path: str):
        await asyncio.to_thread(self.__openai_client.download_results, batch.output_file_id, save_path)
        logging.info(f"Downloaded batch results for batch {batch.batch_id} to {save_path}.")

    def __get_save_path(self, batch_id: str) -> str:
        return os.path.join(self.__base_dir, f"{batch_id}.json")


injector = Injector()
test_code_enhancer = injector.get(TestCodeEnhancer)
