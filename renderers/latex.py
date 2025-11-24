# renderers/latex.py
from openai import OpenAI
from config.prompts import LATEX_RENDER_SYSTEM_PROMPT, LATEX_RENDER_USER_PROMPT_TEMPLATE

def render_matrix_to_latex(client: OpenAI, render_task: str, matrix_core):
    user_prompt = LATEX_RENDER_USER_PROMPT_TEMPLATE.format(
        render_task=render_task,
        matrix_latex_core=matrix_core
    )
    
    resp = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": LATEX_RENDER_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    # llm raw output
    output_text = resp.output[0].content[0].text.strip()

    # check matrix keyword, used in math env
    matrix_keywords = ["bmatrix", "pmatrix", "vmatrix", "matrix", "smallmatrix"]
    has_matrix = any(f"\\begin{{{kw}}}" in output_text for kw in matrix_keywords)


    # check wrapper
    is_wrapped = (
        output_text.strip().startswith("\\[") or 
        output_text.strip().startswith("$") or 
        "\\begin{equation}" in output_text or
        "\\begin{table}" in output_text or  
        "\\begin{figure}" in output_text
    )
    # add math wrapper if raw matrix 
    if has_matrix and not is_wrapped:
        output_text = f"\\[\n{output_text}\n\\]"

    return output_text
