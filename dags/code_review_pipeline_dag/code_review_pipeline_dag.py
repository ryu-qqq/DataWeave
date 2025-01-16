from dags.dag_factory import create_dag

dag_id = "code_review_pipeline"

# 태스크 정의
task_definitions = [

]

dag = create_dag(
    dag_id=dag_id,
    schedule_interval=None,
    task_definitions=task_definitions,
)

globals()[dag_id] = dag
