from injector import Injector, singleton, inject

from modules.generate_ai.executor.executor_provider import ExecutorProvider
from modules.generate_ai.models.code import Code
from modules.generate_ai.models.open_ai_enums import CodeType, PerformerType
from modules.generate_ai.models.task_context_factory_provider import TaskContextFactoryProvider
from modules.generate_ai.models.test_review_report import TestCodeReport
from modules.generate_ai.prompter.test_code_prompter import JavaTestCodePrompter
from modules.generate_ai.tester.tester import Tester


@singleton
class JavaTester(Tester):

    @inject
    def __init__(self, factory_provider: TaskContextFactoryProvider, executor_provider: ExecutorProvider):
        super().__init__(JavaTestCodePrompter())
        self.__factory_provider = factory_provider
        self.__executor_provider = executor_provider

    def supports(self, code: Code) -> bool:
        return code.code_type == CodeType.JAVA

    def write_tests(self, code: Code) -> TestCodeReport:

        system_message, user_message = self._prompter.generate_prompt(code.source)

        factory = self.__factory_provider.get_factory(code.ai_type)
        if factory is None:
            raise ValueError(f"No TaskContextFactory found for AI type: {code.ai_type}")

        task_context = factory.create_context(
            system_message=system_message,
            user_message=user_message,
            perform_type=PerformerType.TESTER
        )

        executor = self.__executor_provider.get_executor(task_context)
        if executor is None:
            raise ValueError("No suitable executor found for the provided TaskContext.")

        return executor.execute(task_context)


injector = Injector()
java_tester = injector.get(JavaTester)
