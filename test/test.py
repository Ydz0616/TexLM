import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from main import run_demo
from dsl.evaluate import evaluate
import ast
import yaml
import numpy as np
import re
from constraints.generate_constraint import generate_constraint

"""
1. Get prompts from input file
2. Collect raw answers to prompts - save the matrix values themselves as well as the latex
3. Get expected answers from input file and compare to raw answers from synthesizer
4. Render the latex
"""

ABS_TOLERANCE = 1e-2
REL_TOLERANCE = 1e-2

def get_matrix(latex_matrix : str) -> np.ndarray:
    latex_matrix = re.sub(r"\\begin\{[A-Za-z]+\}", "", latex_matrix)
    latex_matrix = re.sub(r"\\end\{[A-Za-z]+\}", "", latex_matrix)

    matrix_rows = latex_matrix.split("\\")

    matrix = []
    for row in matrix_rows:
        numbers_as_strings = row.split("&")
        numbers = np.array([np.float64(n) for n in numbers_as_strings])
        matrix.append(numbers)
    
    matrix = np.array(matrix)
    return matrix

def validate(returned_matrix : np.ndarray, expected_matrix : np.ndarray, output_latex_file):
    pass

def test():
    error_count = 0
    with open("test-errors.log", "w") as error_log:
        error_log.write("\n")


# Test well-formatted prompts: these should produce valid latex tables, which are written to well-formatted-prompts-output.tex
        with open("well-formatted-prompts.yaml", "r") as f:
            data = yaml.safe_load(f)
        tests = data["tests"]

        with open("well-formatted-prompts-output.tex", "w") as output_latex_file:
            output_latex_file.write(
"""
\documentclass{article}

\\begin{document}

"""
            )

        
            for t in tests:
                prompt = t["prompt"]

                out = run_demo(prompt)
            
                if out.get("status") == "SUCCESS":
                    returned_matrix = get_matrix(out.get("latex_core"))
                    
                    try:
                        expected_matrix = evaluate(ast.parse(t["expected_program"]))
                    except Exception as e:
                        error_count += 1
                        error_log.write(f"{prompt}")
                        error_log.write(f"Invalid expected program:\n\t {t["expected_program"]}\n")
                        error_log.write(f"Got error: {str(e)}")
                        continue

                    equal = False
                    try:
                        equal = np.allclose(returned_matrix, expected_matrix, rtol=REL_TOLERANCE, atol=ABS_TOLERANCE)
                    except Exception as e:
                        error_count += 1
                        error_log.write(f"{prompt}")
                        error_log.write("Matrices are not comparable.\n")
                        error_log.write("Returned matrix: \n")
                        error_log.write(f"{returned_matrix}\n")
                        error_log.write("but expected matrix: \n")
                        error_log.write(f"{expected_matrix}\n\n\n")
                        continue

                    if equal:
                        output_latex_file.write(f"{prompt}\n")
                        output_latex_file.write(f"{out["final_latex"]}\n\n")
                    else:
                        error_count += 1
                        error_log.write(f"{prompt}")
                        error_log.write("Returned matrix: \n")
                        error_log.write(f"{returned_matrix}\n")
                        error_log.write("but expected matrix: \n")
                        error_log.write(f"{expected_matrix}\n\n\n")
                        
                elif out.get("status") == "NEEDS_REPHRASING":
                    error_count += 1
                    error_log.write(f"{prompt}\n")
                    error_log.write("\n=== FAILED TO GENERATE VALID RESULT ===\n")
                    error_log.write(f"Reason: {out.get('error_reason')}\n\n")
                else:
                    error_count += 1
                    error_log.write(f"{prompt}\n")
                    error_log.write("\n=== SYSTEM ERROR ===\n")
                    error_log.write(f"{out}")
        
            output_latex_file.write(
"""

\end{document}
"""
            )

# Test poorly-formatted prompts
        with open("poorly-formatted-prompts.yaml", "r") as f:
            data = yaml.safe_load(f)
        tests = data["tests"]

        with open("poorly-formatted-prompts-output.txt", "w") as output_latex_file:
            
            for t in tests:
                prompt = t["prompt"]

                out = run_demo(prompt)
            
                if out.get("status") == "SUCCESS":
                    output_latex_file.write(f"{prompt}\n")
                    output_latex_file.write(f"Did not expect prompt to produce valid output. Expected output:\n{t["expected_reason"]}\n\n")
                elif out.get("status") == "NEEDS_REPHRASING":
                    output_latex_file.write(f"{prompt}\n")
                    output_latex_file.write("Outputted reason:\n")
                    output_latex_file.write("\t=== FAILED TO GENERATE VALID RESULT ===\n")
                    output_latex_file.write(f"\tReason: {out.get('error_reason')}\n\n")
                    output_latex_file.write("Expected reason (more or less):\n")
                    output_latex_file.write(f"\t{t["expected_reason"]}\n\n")
                else:
                    output_latex_file.write(f"{prompt}\n")
                    output_latex_file.write("\t=== SYSTEM ERROR ===\n")
                    output_latex_file.write(f"\t{out}\n\n")

# Test adversarial prompts
        with open("adversarial-prompts.yaml", "r") as f:
            data = yaml.safe_load(f)
        tests = data["tests"]

        with open("adversarial-prompts-output.txt", "w") as output_latex_file:
            
            for t in tests:
                prompt = t["prompt"]

                out = run_demo(prompt)
            
                if out.get("status") == "SUCCESS":
                    output_latex_file.write(f"{prompt}\n")
                    output_latex_file.write(f"This prompt produced the following output:\n{out.get("latex_core")}\n")
                    # output_latex_file.write("It should have returned an error.\n\n")
                elif out.get("status") == "NEEDS_REPHRASING":
                    output_latex_file.write(f"{prompt}\n")
                    output_latex_file.write("Outputted error:\n")
                    output_latex_file.write("\t=== FAILED TO GENERATE VALID RESULT ===\n")
                    output_latex_file.write(f"\tReason: {out.get('error_reason')}\n\n")
                else:
                    output_latex_file.write(f"{prompt}\n")
                    output_latex_file.write("Outputted error:\n")
                    output_latex_file.write("\t=== SYSTEM ERROR ===\n")
                    output_latex_file.write(f"\t{out}\n\n")

# Finish error log
    with open("test-errors.log", "r") as error_log:
        lines = error_log.readlines()
        
    lines[0] = f"Error count: {error_count}\n\n\n"
    
    with open("test-errors.log", "w") as error_log:
        error_log.writelines(lines)



if __name__ == "__main__":
    test()