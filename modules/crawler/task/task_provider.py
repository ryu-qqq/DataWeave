from modules.crawler.task.crawl_task_executor import crawl_task_executor
from modules.crawler.task.process_task_executor import process_task_executor
from modules.crawler.task.task_interface import TaskInterface
from modules.crawler.process_type import Process


class TaskProvider:

    @staticmethod
    def get_task_provider(task_type: str) -> TaskInterface:
        if task_type == Process.CRAWLING.name:
            return crawl_task_executor
        elif task_type == Process.PROCESSING.name:
            return process_task_executor

        raise ValueError(f"Unsupported task type: {task_type}")