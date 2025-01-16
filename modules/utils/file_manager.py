import json
import logging
import os

import aiofiles


class FileManager:

    @staticmethod
    def cleanup_downloaded_file(file_path: str):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logging.info(f"Deleted downloaded file: {file_path}")
        except Exception as e:
            logging.error(f"Error deleting file {file_path}: {e}")

    @staticmethod
    async def save_json_to_file(data: dict, save_path: str):
        async with aiofiles.open(save_path, mode='w', encoding='utf-8') as file:
            await file.write(json.dumps(data, ensure_ascii=False))
        logging.info(f"Saved JSON data to {save_path}")