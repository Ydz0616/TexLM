# main.py
import ast
from config.config import get_client
from dsl.evaluate import evaluate
from renderers.latex import render_matrix_to_latex
# NOTE: Decomposer is removed
from dsl.generator import generate_dsl_and_format 
from dsl.verify import verify
from constraints.generate_constraint import generate_constraint

def run_demo(user_msg: str):
    client = get_client()

    print(f"\n[1/3] Super-Parsing (NLP -> DSL)...")
    try:
        # === Core Call: One-Pass Generation ===
        parsed = generate_dsl_and_format(client, user_msg)
        
        dsl = parsed["dsl"]
        formatting = parsed["formatting"]
        reasoning = parsed["reasoning"]
        
        print(f"   AI Thought: {reasoning}...") 
        print(f"   Detected Format: {formatting}")
        print(f"   Generated DSL: {dsl}")
        
    except Exception as e:
        print(f"Generation Error: {e}")
        return None

    # === Self-Verification (Verifier) ===
    print(f"\n[2/3] Verifying Logic...")
    # Verify the DSL against the original user message
    verification = verify(client, "gpt-4o", user_msg, dsl) 

    if not verification["is_valid"]:
        print(f"Verification Failed: {verification['explanation']}")
        # TODO: Implement Retry Loop here if needed
        return None
    else:
        print(f"   Verified: {verification['explanation']}")

    # === Execution & Rendering ===
    print(f"\n[3/3] Executing & Rendering...")
    try:
        # 1. Parse DSL to AST
        program_ast = ast.parse(dsl)
        
        # 2. Calculate Result (Numpy)
        result_matrix = evaluate(program_ast)
        print("   Calculation Successful.")

        # 3. Generate Regex/Constraint (Absolute Correct LaTeX Core)
        latex_core = generate_constraint(result_matrix)
        
        # 4. Final Render (Wrap core in formatting)
        final_latex = render_matrix_to_latex(client, formatting, latex_core)

        return {
            "reasoning": reasoning,
            "dsl": dsl,
            "latex_core": latex_core,
            "final_latex": final_latex
        }

    except Exception as e:
        print(f"Execution Error: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Test case: complex logic to test if "multiplication" is captured
    user_msg = "give me a latex table of the inverse of the transpose of the multiplication of matrix ([1,5] ,[3,4]) and matrix ([4,5] ,[6,7])"
    
    out = run_demo(user_msg)
    
    if out and "final_latex" in out:
        print("\n=== FINAL OUTPUT ===")
        print(out["final_latex"])