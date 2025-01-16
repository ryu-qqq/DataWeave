from modules.generate_ai.executor.open_ai_executor import OpenAiExecutor
from modules.generate_ai.models.open_ai_task_context import OpenAiTaskContext

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)

    # OpenAiTaskContext 생성
    context = OpenAiTaskContext(
        system_message=(
            "You are Robert C. Martin, a renowned expert in clean code principles. "
            "Review the following Java code and provide feedback in JSON format:\n"
            "{\n"
            '  "review": "<Review of the original code>",\n'
            '  "suggested_code": "<Improved version of the code>"\n'
            "}\n"
        ),
        user_message="public class Calculator { public int add(int a, int b) { return a + b; } }",
        is_realtime=True,
    )

    # OpenAiExecutor 초기화
    executor = OpenAiExecutor()

    # 실행
    result = executor.execute(context)
    print("=== Execution Result ===")
    print(result)
