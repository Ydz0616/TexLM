   # main.py
from config.config import get_client
from dsl.parser import parse_dsl
from renderers.latex import render_matrix_to_latex
from renderers.decompose import decompose_user_message

# NEW: generator.py
from dsl.generator import generate_dsl


def run_demo(user_msg: str):
    # 1) Obtain Openai Client
    client = get_client()

    # 1) Parse natural language input into structured components
    decomp = decompose_user_message(client, user_msg)
    # decomp contains: formatting, instruction, matrix

    # 2) Generate DSL with instruction and matrix data
    dsl = generate_dsl(client, decomp.instruction, decomp.matrix)

    # TODO: do the rest :

    # # 5) pase DSL to AST
    # ast_dsl = parse_dsl(dsl)

    # # 6) Execute AST and do Calculation
    # result = task.execute(ast_dsl, matrix)

    # # 7) Implement Rendering
    # latex = render_matrix_to_latex(client, decomp.formatting, result)

    return {
        "decomposition": {
            "formatting": decomp.formatting,
            "instruction": decomp.instruction,
            "matrix": decomp.matrix,
        },
        "dsl": dsl,
        # "result": result,
        # "latex": latex,
    }

if __name__ == "__main__":
    # Example natural language input
    user_msg = "give me a latex table with width = 70% for overleaf for inverse of the transpose of the multiplication of matrix ([1,2] ,[3,4]) and  matrix ([4,5] ,[6,7]) "
    
    out = run_demo(user_msg)
    print("=== Decomposition ===")
    print(f"Formatting: {out['decomposition']['formatting']}")
    print(f"Instruction: {out['decomposition']['instruction']}")
    print(f"Matrix: {out['decomposition']['matrix']}")
    print("\n=== DSL ===")
    print(out["dsl"])
