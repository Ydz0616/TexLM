   # main.py
from config.config import get_client
from dsl.verify import verify
from dsl.evaluate import evaluate
from renderers.latex import render_matrix_to_latex
from renderers.decompose import decompose_user_message
from dsl.generator import generate_dsl
# Parse DSL to AST
import ast 

# NEW: generate regex constraint
from constraints.generate_constraint import generate_constraint


def run_demo(user_msg: str):

    # 1) Obtain Openai Client
    client = get_client()

    
    # 1) Parse natural language input into structured components

    print(f"--- 1. Decomposing user message ---")
    decomp = decompose_user_message(client, user_msg)

    # 2) Generate DSL with instruction and matrix data
    print(f"--- Genrating DSL ---")
    dsl = generate_dsl(client, decomp.instruction, decomp.matrix)

    # NEW: VERIFY DSL WITH LLM 
    verification = verify(client=client, model="gpt-4o",user_instruction=decomp.instruction, dsl_code=dsl)
    # TODO: 1. Multiple Rounds of Verification if not successful
    # TODO: 2. Include user in the loop if still not successful after multiple rounds of verification/


    if not verification["is_valid"]:
        print(f"\n❌ [BLOCKING ERROR] DSL Mismatch!")
        print(f"   User asked for: {decomp.instruction}")
        print(f"   AI generated:   {dsl}")
        print(f"   Verifier Analysis: {verification['explanation']}")
        return None
    
    program_ast = ast.parse(dsl)
    print(f"--- The Generated DSL is {dsl} ---")

    try:

    # 5) parse DSL to AST
    
        program_ast = ast.parse(dsl)

        # calculate the matrix using our built-in calculator
        result_matrix = evaluate(program_ast)
        print("--- Calculation Successful ---")

        # get the regex constraint
        result_latex_core = generate_constraint(result_matrix)
        print(f"---result latex regex: {result_latex_core} --- ")

    except Exception as e:
        print("Caught unexpected error:", type(e).__name__, e)
        return {
            "error":str(e),
            "dsl":dsl
                }
        # TODO: maybe feed this back into the LLM (something about the program was wrong)

    # # 7) Implement Rendering
    final_latex = render_matrix_to_latex(client, decomp.formatting, result_latex_core)

    return {
        "decomposition": {
            "formatting": decomp.formatting,
            "instruction": decomp.instruction,
            "matrix": decomp.matrix,
        },
        "dsl": dsl,
        "result_matrix": result_matrix, 
        "latex_core": result_latex_core,
        "final_latex": final_latex
    }

if __name__ == "__main__":
    # Example natural language input
    user_msg = """Give me a latex matrix of the inverse of the transpose
    of the multiplication of matrix ([1,2] ,[3,4]) and  matrix ([4,5] ,[6,7]) """
    
    out = run_demo(user_msg)
    if out and "error" not in out:
        print("\n=== ✅ SUCCESS ===")
        print(f"DSL Logic:   {out['dsl']}")
        print(f"Latex Core:  {out['latex_core']}")  # check if this is a standard matrix
        print(f"Final Latex: \n{out['final_latex']}")
    else:
        print("\n=== ❌ FAILED ===")
        print(out)

