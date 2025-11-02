# schemas.py
from pydantic import BaseModel
from typing import List, Optional

class TaskArgs(BaseModel):
    model_config = {"extra": "forbid"}   # pydantic v2 


class Decomposition(BaseModel):

    matrix_data: str
    # LLM must give a task name
    task_name: str
    # saving other args for add/multiply
    task_args: Optional[TaskArgs] = None
    # rendering layer
    render_task: str
