import ast
import textwrap
from config.config import get_client
from dsl.evaluate import evaluate
from renderers.latex import render_matrix_to_latex
from dsl.generator import generate_dsl_and_format 
from dsl.verify import verify
from constraints.generate_constraint import generate_constraint

# === Configuration ===
MAX_RETRIES = 1  # Total attempts = 1 (initial) + 2 (retries)

def execute_pipeline(client, dsl, formatting="latex matrix"):
    """
    Executes the DSL -> AST -> Numpy -> Constraint -> Latex pipeline.
    Returns a dictionary indicating success or failure (execution error).
    """
    try:
        # 1. Parse DSL to AST
        program_ast = ast.parse(dsl)
        
        # 2. Calculate Result (Numpy)
        # This step might raise ValueError (dimension mismatch) or LinAlgError (singular matrix)
        result_matrix = evaluate(program_ast)
        
        # 3. Generate Regex/Constraint (Absolute Correct LaTeX Core)
        latex_core = generate_constraint(result_matrix)
        
        # 4. Final Render (Wrap core in formatting)
        final_latex = render_matrix_to_latex(client, formatting, latex_core)

        return {
            "status": "SUCCESS",
            "dsl": dsl,
            "final_latex": final_latex,
            "latex_core": latex_core
        }

    except Exception as e:
        # Capture execution errors (Math errors, Syntax errors, etc.)
        return {
            "status": "ERROR",
            "error": str(e)
        }

def run_demo(user_msg: str):
    client = get_client()

    # Initialization
    current_user_prompt = user_msg
    dsl = ""
    formatting = "latex matrix"
    reasoning = ""
    last_error_explanation = ""

    print(f"\n[System] Starting Task. Max Retries: {MAX_RETRIES}")

    # === Retry Loop ===
    for attempt in range(MAX_RETRIES + 1):
        attempt_label = f"Attempt {attempt + 1}/{MAX_RETRIES + 1}"
        print(f"\n--- {attempt_label} ---")

        # 1. Generate (Super-Parsing)
        try:
            if attempt > 0:
                print("[Generator] Retrying with error feedback...")
            else:
                print("[Generator] Parsing user request...")

            # Call the Super-Generator
            parsed = generate_dsl_and_format(client, current_user_prompt)
            
            dsl = parsed["dsl"]
            formatting = parsed["formatting"]
            reasoning = parsed["reasoning"]

            if not dsl:
                # model refuse to generate dsl
                return {
                    "status": "NEEDS_REPHRASING",
                    "reasoning": reasoning,
                    "failed_dsl": "N/A (Model refused to generate)",
                    "error_reason": "The model could not parse a valid matrix from your input. See the thought process."
                }

            print(f"  Detected Format: {formatting}")
            print("   AI Thought:")
            print(textwrap.fill(reasoning, width=80, initial_indent="      ", subsequent_indent="      "))
            print(f"  Generated DSL: {dsl}")

        except Exception as e:
            return {"status": "ERROR", "error": f"Generation failed: {str(e)}"}

        # 2. Verify Logic (LLM Verification)
        print("[Verifier] Checking logic...")
        # CRITICAL: Always verify against the ORIGINAL user message to ensure intent match
        verification = verify(client, "gpt-4o", user_msg, dsl)

        execution_result = None
        is_success = False

        if verification["is_valid"]:
            print(f"   PASS: {verification['explanation']}")
            
            # 3. Verify Execution (Pre-flight Check)
            # Even if logic looks right, math might fail (e.g. dimension mismatch)
            print("[Execution] Attempting to execute...")
            execution_result = execute_pipeline(client, dsl, formatting)
            
            if execution_result["status"] == "SUCCESS":
                # Both Logic and Math are correct
                is_success = True
            else:
                # Logic passed, but Math failed
                print(f"   FAIL (Execution): {execution_result['error']}")
                last_error_explanation = f"Execution Error: {execution_result['error']}"
        else:
            # Logic failed
            print(f"   FAIL (Verifier): {verification['explanation']}")
            last_error_explanation = verification['explanation']

        # === Decision Logic ===
        if is_success:
            # Success! Return the result
            execution_result["reasoning"] = reasoning
            return execution_result
        
        else:
            # Failure: Prepare for retry if possible
            if attempt < MAX_RETRIES:
                print("[System] Preparing feedback for next attempt...")
                current_user_prompt = (
                    f"{user_msg}\n\n"
                    f"[System Feedback]: Your previous DSL '{dsl}' was INCORRECT.\n"
                    f"Error Detail: {last_error_explanation}\n"
                    f"Please fix this error in your next attempt."
                )
            else:
                print("\n[System] Max retries reached. Auto-correction failed.")

    # === Final Failure (Loop Ended) ===
    # Return context so UI can explain WHY it failed and ask user to rephrase
    return {
        "status": "NEEDS_REPHRASING", 
        "reasoning": reasoning,
        "failed_dsl": dsl,
        "error_reason": last_error_explanation,
        "formatting": formatting
    }

if __name__ == "__main__":
    # Test case: complex nesting to trigger potential retry
    user_msg = """give me a latex table of the inverse of the transpose of the multiplication of matrix ([
    1,-2] ,[3,4]) and matrix ([4,5] ,[6,7]"")"""

    # Edge case: dimension mismatch (should trigger internal retries and eventual failure info)
    # user_msg = "multiply matrix [[1,2,3],[4,5,6]] and matrix [[2,3,4],[4,5,2]]"

    out = run_demo(user_msg)
    
    if out.get("status") == "SUCCESS":
        print("\n=== FINAL OUTPUT ===")
        print(out["final_latex"])
    elif out.get("status") == "NEEDS_REPHRASING":
        print("\n=== FAILED TO GENERATE VALID RESULT ===")
        print(f"Reason: {out.get('error_reason')}")
    else:
        print("\n=== SYSTEM ERROR ===")
        print(out)