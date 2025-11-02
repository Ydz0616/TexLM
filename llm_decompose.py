# llm_decompose.py
from typing import Tuple
from openai import OpenAI
from schemas import Decomposition

SYSTEM_MSG = (
    "You read user messages about MATRIX operations.\n"
    "You must output JSON with:\n"
    "- matrix_data: the matrix (normalize to [[...], [...]])\n"
    "- task_name: one of ['transpose', 'matmul', 'add'] (pick the best match)\n"
    "- task_args: extra info for the task (can be null)\n"
    "- render_task: formatting requirements (LaTeX, etc.)\n"
    "If the user only gives ONE matrix and says 'transpose', task_name='transpose'.\n"
    "If the user says 'multiply A and B', task_name='matmul' and put the second matrix in task_args.\n"
)

def decompose_user_message(client: OpenAI, user_text: str) -> Decomposition:
    resp = client.responses.parse(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": SYSTEM_MSG},
            {"role": "user", "content": user_text},
        ],
        text_format=Decomposition,
    )
    return resp.output_parsed

