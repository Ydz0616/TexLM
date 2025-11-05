# renderers/latex.py
from openai import OpenAI
from config.prompts import LATEX_RENDER_SYSTEM_PROMPT, LATEX_RENDER_USER_PROMPT_TEMPLATE

def render_matrix_to_latex(client: OpenAI, render_task: str, matrix):
    user_prompt = LATEX_RENDER_USER_PROMPT_TEMPLATE.format(
        render_task=render_task,
        matrix=matrix
    )

    resp = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": LATEX_RENDER_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return resp.output[0].content[0].text.strip()
