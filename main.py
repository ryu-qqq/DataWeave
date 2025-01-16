import asyncio

from modules.gpt.models.product_data_type import BatchDataType
from modules.gpt.batch_processor import batch_processor

if __name__ == "__main__":

    #asyncio.run(batch_status_checker.check_and_update_batch_states())
    #asyncio.run(completed_batch_handler.process_completed_batches())
    #asyncio.run(test_code_enhancer.enhance())

    asyncio.run(batch_processor.process(
        fetch_params={
                    "status": "PENDING",
                    "change_types": ["ADDED", "MODIFIED"],
                    "page_size": 20,
                    "page_number": 0,
                    "cursor": None,
                    "sort": "ASC"
                },
        batch_data_type=BatchDataType.TEST_CODE
    ))

