import logging

from injector import singleton, inject, Injector

from modules.generate_ai.client.real_time_open_ai_client import real_time_open_api_client
from modules.generate_ai.executor.executor import Executor
from modules.generate_ai.executor.report_generator_provider import ReportGeneratorProvider
from modules.generate_ai.models.open_ai_task_context import OpenAiTaskContext
from modules.generate_ai.models.report import Report


@singleton
class OpenAiExecutor(Executor[OpenAiTaskContext]):

    @inject
    def __init__(self, report_generator_provider: ReportGeneratorProvider):
        self.__client = None
        self.__report_generator_provider = report_generator_provider

    def supports(self, context: OpenAiTaskContext) -> bool:
        return isinstance(context, OpenAiTaskContext)

    def _initialize_client(self):
        if self.__client is None:
            try:
                logging.info("Initializing RealTimeOpenAIClient...")
                self.client = real_time_open_api_client
            except Exception as e:
                logging.error(f"Failed to initialize RealTimeOpenAIClient: {e}")
                raise

    def execute(self, context: OpenAiTaskContext) -> Report:
        if not self.supports(context):
            raise ValueError("Unsupported TaskContext for OpenAiExecutor.")

        if context.is_realtime:
            self._initialize_client()
        else:
            raise ValueError("Batch client is not yet supported.")

        logging.info("Executing task with OpenAI (real-time)...")
        response = self.client.generate_prompt(
            system_message=context.system_message,
            user_message=context.user_message,
            model=context.model,
            temperature=context.temperature,
        )
        generator = self.__report_generator_provider.get_generator(context.perform_type)

        return generator.generate(response)


injector = Injector()
open_ai_executor = injector.get(OpenAiExecutor)
