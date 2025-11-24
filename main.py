import ast
import textwrap
from config.config import get_client
from dsl.evaluate import evaluate
from renderers.latex import render_matrix_to_latex
from dsl.generator import generate_dsl_and_format 
from dsl.verify import verify
from constraints.generate_constraint import generate_constraint

# === Configuration ===
MAX_RETRIES = 2  # Total attempts = 1 (initial) + 2 (retries)

def run_demo(user_msg: str):
    client = get_client()

    # Initialize variables for the loop
    current_user_prompt = user_msg
    dsl = ""
    formatting = "latex matrix"
    reasoning = ""
    last_error_explanation = ""
    verification_passed = False

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

            print(f"   Detected Format: {formatting}")
            print("   AI Thought:")
            print(textwrap.fill(reasoning, width=80, initial_indent="      ", subsequent_indent="      "))
            print(f"   Generated DSL: {dsl}")

        except Exception as e:
            print(f"[Error] Generation failed: {e}")
            return None

        # 2. Verify
        print("[Verifier] Checking logic...")
        # CRITICAL: Always verify against the ORIGINAL user message to ensure intent match
        verification = verify(client, "gpt-4o", user_msg, dsl)

        if verification["is_valid"]:
            print(f"   PASS: {verification['explanation']}")
            verification_passed = True
            break  # Success! Exit loop
        else:
            print(f"   FAIL: {verification['explanation']}")
            last_error_explanation = verification['explanation']
            
            # If this was the last attempt, don't construct retry prompt, just break
            if attempt == MAX_RETRIES:
                print("\n[System] Max retries reached. Auto-correction failed.")
                break
            
            # 3. Construct Feedback for Next Attempt (Prompt Injection)
            print("[System] Preparing feedback for next attempt...")
            current_user_prompt = (
                f"{user_msg}\n\n"
                f"[System Feedback]: Your previous generated DSL '{dsl}' was INCORRECT.\n"
                f"Verifier Error: {last_error_explanation}\n"
                f"Please fix this error in your next attempt."
            )

    # === Human-in-the-loop (Fallback) ===
    # If we exited the loop but verification is still False
    if not verification_passed:
        print("\n" + "="*40)
        print("HUMAN INTERVENTION REQUIRED")
        print("="*40)
        print(f"User Request: {user_msg}")
        print(f"Last Failed DSL: {dsl}")
        print(f"Reason: {last_error_explanation}")
        
        user_override = input("\nPlease enter the correct DSL manually (or press Enter to abort): ").strip()
        
        if user_override:
            dsl = user_override
            print(f"   Using Human-Provided DSL: {dsl}")
        else:
            print("   Operation Aborted.")
            return None

    # === Execution & Rendering ===
    print("\n[Execution] Calculating results...")
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
        print(f"[Error] Execution failed: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Test case: complex nesting to trigger potential retry
    user_msg = """give me a latex table of the inverse of the transpose of the multiplication of matrix ([
    1,-2] ,[3,4]) and matrix ([4,5] ,[6,7]"")"""

    # edge case: this would lead to fast failure ( DSL gen error), which is what we expected
    # user_msg = """I wanna be a carpenter!"""
    

    out = run_demo(user_msg)
    
    if out and "final_latex" in out:
        print("\n=== FINAL OUTPUT ===")
        print(out["final_latex"])