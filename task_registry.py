# task_registry.py
from typing import Dict, Type
from tasks.base import BaseTask
from tasks.transpose import TransposeTask
# from tasks.matmul import MatmulTask  

TASK_REGISTRY: Dict[str, Type[BaseTask]] = {
    "transpose": TransposeTask,
    # "matmul": MatmulTask,
    # "add": AddTask, ...
}

def get_task(task_name: str) -> BaseTask:
    task_cls = TASK_REGISTRY.get(task_name)
    if not task_cls:
        raise ValueError(f"Task '{task_name}' not supported yet.")
    return task_cls()
