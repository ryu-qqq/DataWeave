from injector import singleton, Injector, inject

from modules.generate_ai.executor.executor_provider import ExecutorProvider
from modules.generate_ai.models.code import Code
from modules.generate_ai.models.code_review_report import CodeReviewReport
from modules.generate_ai.models.task_context_factory_provider import TaskContextFactoryProvider
from modules.generate_ai.prompter.code_review_prompter import JavaCodeReviewPrompter
from modules.generate_ai.reviewer.reviewer import Reviewer
from modules.generate_ai.models.open_ai_enums import CodeType, PerformerType


@singleton
class JavaReviewer(Reviewer):

    @inject
    def __init__(self, factory_provider: TaskContextFactoryProvider, executor_provider: ExecutorProvider):
        super().__init__(JavaCodeReviewPrompter())
        self.__factory_provider = factory_provider
        self.__executor_provider = executor_provider

    def supports(self, code: Code) -> bool:
        return code.code_type == CodeType.JAVA

    def review_code(self, code: Code) -> CodeReviewReport:

        system_message, user_message = self._prompter.generate_prompt(code.source)

        factory = self.__factory_provider.get_factory(code.ai_type)
        if factory is None:
            raise ValueError(f"No TaskContextFactory found for AI type: {code.ai_type}")

        task_context = factory.create_context(
            system_message=system_message,
            user_message=user_message,
            perform_type=PerformerType.REVIEWER
        )

        executor = self.__executor_provider.get_executor(task_context)
        if executor is None:
            raise ValueError("No suitable executor found for the provided TaskContext.")

        return executor.execute(task_context)


injector = Injector()
java_reviewer = injector.get(JavaReviewer)