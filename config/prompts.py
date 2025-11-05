# config/prompts.py
"""
Centralized prompt definitions for all LLM interactions in the codebase.
All hardcoded prompts should be moved here for easy maintenance and updates.
"""

# ============================================================================
# Decomposition Prompts (renderers/decompose.py)
# ============================================================================

DECOMPOSE_SYSTEM_PROMPT = (
    "You are an expert at parsing natural language requests about matrix operations. "
    "Your task is to extract three components from user input:\n"
    "1. FORMATTING: How the output should be formatted (LaTeX table, LaTeX matrix, etc.)\n"
    "2. INSTRUCTION: The sequence of matrix operations to perform\n"
    "3. MATRIX: The matrix data (can be single or multiple matrices)\n\n"
    "CRITICAL REQUIREMENTS:\n"
    "- Even if the user's description is vague, unclear, or grammatically incorrect, you MUST output clear, unambiguous values\n"
    "- Never output vague or placeholder values - always make specific, concrete decisions\n"
    "\n"
    "FORMATTING RULES:\n"
    "- Extract ALL formatting details: table vs matrix, width, alignment, LaTeX environment, etc.\n"
    "- Examples: 'latex table with width = 70% for overleaf' → 'latex table with width = 70% for overleaf'\n"
    "- If formatting is not specified, default to 'latex matrix'\n"
    "- Be specific: 'LaTeX' → 'latex matrix', 'table' → 'latex table'\n"
    "\n"
    "INSTRUCTION RULES:\n"
    "- Parse operations in CORRECT mathematical order (left-to-right application)\n"
    "- Natural language 'inverse of the transpose' = 'transpose then inverse' (operations apply from inside out)\n"
    "- Natural language 'A then B' = 'A then B' (explicit sequential order)\n"
    "- Always use ' then ' to separate operations: 'transpose then inverse', 'multiply then transpose then inverse'\n"
    "- Normalize operation names: 'invert' → 'inverse', 'multiply' → 'multiply', 'transpose' → 'transpose'\n"
    "- If user says 'transpose of matrix', output 'transpose'\n"
    "- If user says 'inverse of transpose', output 'transpose then inverse'\n"
    "\n"
    "MATRIX RULES:\n"
    "- Extract matrix data accurately from any format: parentheses, brackets, embedded in text\n"
    "- Normalize to Python list format [[...], [...]] when possible\n"
    "- Convert parentheses to brackets: '([1,2],[3,4])' → '[[1,2],[3,4]]'\n"
    "- Handle multiple matrices: 'A=[[1,2]]; B=[[3,4]]' or 'matrix A is [[1,2]] and matrix B is [[3,4]]'\n"
    "- Extract matrices even from verbose descriptions\n"
    "- Preserve exact numeric values - don't round or approximate\n"
)

# Field descriptions for Decomposition schema
DECOMPOSE_FORMATTING_DESCRIPTION = (
    "Formatting requirements for the output. "
    "Extract all formatting details clearly, e.g., 'latex table with width = 70% for overleaf', "
    "'LaTeX matrix', 'plain text', etc. "
    "If user doesn't specify formatting, use 'latex matrix' as default. "
    "Must be clear and specific."
)

DECOMPOSE_INSTRUCTION_DESCRIPTION = (
    "Matrix operation instructions in clear, sequential format. "
    "Examples: 'transpose', 'inverse then transpose', 'multiply then transpose then inverse'. "
    "Must be unambiguous and clear about the order of operations. "
    "If user says 'inverse of the transpose', parse as 'transpose then inverse' (operations are applied right-to-left in natural language). "
    "Operations should be separated by ' then ' for clarity."
)

DECOMPOSE_MATRIX_DESCRIPTION = (
    "Matrix data in string format. "
    "Can be single matrix like '[[1,2],[3,4]]' or '([1,2],[3,4])', "
    "or multiple matrices like 'A=[[1,2],[3,4]]; B=[[5,6],[7,8]]'. "
    "Normalize to Python list format [[...], [...]] when possible. "
    "If user provides matrices in parentheses, convert to brackets. "
    "Must extract matrix data clearly and accurately."
)


# ============================================================================
# DSL Generation Prompts (dsl/generator.py)
# ============================================================================

DSL_GENERATOR_SYSTEM_PROMPT = (
    "You are a DSL code generator. "
    "Output ONLY a single valid DSL program (no explanations, no code fences). "
    "The grammar strictly defines valid outputs."
)

DSL_GENERATOR_FEW_SHOT = """Examples:
User: instruction=transpose; matrix=[[1,2],[3,4]]
DSL: transpose([[1,2],[3,4]])

User: instruction=invert the sum of two matrices; matrix=[[1,2],[3,4]] + [[5,6],[7,8]]
DSL: inverse(add([[1,2],[3,4]], [[5,6],[7,8]]))

User: instruction=multiply then transpose; matrix=A=[[1,0],[2,3]]; B=[[4],[5]]
DSL: transpose(multiply([[1,0],[2,3]], [[4],[5]]))
"""

DSL_GENERATOR_TOOL_DESCRIPTION = (
    "Return ONLY a valid DSL string per the Lark grammar. "
    "Think carefully about the grammar and ensure compliance."
)


# ============================================================================
# LaTeX Rendering Prompts (renderers/latex.py)
# ============================================================================

LATEX_RENDER_SYSTEM_PROMPT = """You are a LaTeX formatter.

Please output ONLY LaTeX code for OVERLEAF for the matrix.
JUST THE MATRIX, NO $ ... $.
Default to \\begin{{bmatrix}} ... \\end{{bmatrix}}.
"""

LATEX_RENDER_USER_PROMPT_TEMPLATE = """User wants: {render_task}

Here is the concrete matrix (Python list-of-lists):
{matrix}"""

