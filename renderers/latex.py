# renderers/latex.py
from openai import OpenAI

def render_matrix_to_latex(client: OpenAI, render_task: str, matrix):
    prompt = f"""
You are a LaTeX formatter.

User wants: {render_task}

Here is the concrete matrix (Python list-of-lists):
{matrix}

Please output ONLY LaTeX code for OVERLEAF for this matrix.
JUST THE MATRIX, NO $ ... $.
Default to \\begin{{bmatrix}} ... \\end{{bmatrix}}.
""".strip()

    resp = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
    )
    return resp.output[0].content[0].text.strip()
