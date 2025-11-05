   # main.py
import ast

from config import get_client
from llm_decompose import decompose_user_message
from task_registry import get_task
from dsl.parser import parse_dsl
from renderers.latex import render_matrix_to_latex

def normalize_matrix_literal(lit: str):
    lit = lit.strip()
    # formatting split -- could edit later for better support
    if lit.startswith("(") and lit.endswith(")"):
        lit = lit[1:-1]
        lit = "[" + lit + "]"
    return ast.literal_eval(lit)

def run_demo(user_msg: str):
    client = get_client()

    # 1) LLM #1: detects instruction
    decomp = decompose_user_message(client, user_msg)
    # decomp: Decomposition

    # 2) normalize/re-format the matrix
    matrix = normalize_matrix_literal(decomp.matrix_data)

    # 3) get the task according to what we detected
    task = get_task(decomp.task_name)

    # 4) generate the DSL
    dsl = task.build_dsl(decomp.model_dump(), matrix)

    # 5) pase our dsl
    ast_dsl = parse_dsl(dsl)

    # 6) execuate the job
    result = task.execute(ast_dsl, matrix)

    # 7) rendering
    latex = render_matrix_to_latex(client, decomp.render_task, result)

    return {
        "decomposition": decomp.model_dump(),
        "dsl": dsl,
        "result": result,
        "latex": latex,
    }

if __name__ == "__main__":
    user_msg = "I have ([1,2],[3,4]). Please generate its transpose matrix, in LaTeX, and don't overflow."
    out = run_demo(user_msg)
    print("=== decomposition ===")
    print(out["decomposition"])
    print("=== DSL ===")
    print(out["dsl"])
    print("=== result ===")
    print(out["result"])
    print("=== LaTeX ===")
    print(out["latex"])
