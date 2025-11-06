   # main.py
from config.config import get_client
from dsl.parser import parse_dsl
from dsl.evaluate import evaluate
from renderers.latex import render_matrix_to_latex
from renderers.decompose import decompose_user_message
import ast

# NEW: generator.py
from dsl.generator import generate_dsl


def run_demo(user_msg: str):
    # tree = ast.parse("[[1,2],[3,4]]")

    # 1) Obtain Openai Client
    client = get_client()

    # 1) Parse natural language input into structured components
    decomp = decompose_user_message(client, user_msg)
    # decomp contains: formatting, instruction, matrix

    # 2) Generate DSL with instruction and matrix data
    dsl = generate_dsl(client, decomp.instruction, decomp.matrix)

    # TODO: do the rest :

    # 5) pase DSL to AST
    program_ast = ast.parse(dsl)

    # 6) Evaluate AST and do Calculation
    try:
        result = evaluate(program_ast)
    except Exception as e:
        print("Caught unexpected error:", type(e).__name__, e)
        return None
        # TODO: maybe feed this back into the LLM (something about the program was wrong)

    # # 7) Implement Rendering
    # latex = render_matrix_to_latex(client, decomp.formatting, result)

    return {
        "decomposition": {
            "formatting": decomp.formatting,
            "instruction": decomp.instruction,
            "matrix": decomp.matrix,
        },
        "dsl": dsl,
        "result": result,
        # "result": result,
        # "latex": latex,
    }

if __name__ == "__main__":
    # Example natural language input
    user_msg = "give me a latex table of the inverse of the transpose of the multiplication of matrix ([1,2] ,[3,4]) and  matrix ([4,5] ,[6,7]) "
    
    out = run_demo(user_msg)
    print("=== User Message ===")
    print(f"User Message:{user_msg}")
    print("=== Decomposition ===")
    print(f"Formatting: {out['decomposition']['formatting']}")
    print(f"Instruction: {out['decomposition']['instruction']}")
    print(f"Matrix: {out['decomposition']['matrix']}")
    print("\n=== DSL ===")
    print(out["dsl"])
    print("\n=== Result ===")
    print(out["result"])
