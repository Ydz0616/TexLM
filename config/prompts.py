# config/prompts.py
"""
Centralized prompt definitions for all LLM interactions in the codebase.
All hardcoded prompts should be moved here for easy maintenance and updates.
"""

# ============================================================================
# Decomposition Prompts (renderers/decompose.py)
# ============================================================================
# config/prompts.py

# ============================================================================
# Decomposition Prompts (renderers/decompose.py)
# ============================================================================

DECOMPOSE_SYSTEM_PROMPT = """You are an expert parsing engine for matrix operations.
Extract three structured components from the user's natural language request.

1. **FORMATTING**: The visual output style (e.g., 'latex table', 'bmatrix').
   - Default to 'latex matrix' if unspecified.
   - Be specific (e.g., capture 'width=70%', 'for overleaf').

2. **MATRIX**: The raw matrix data.
   - Normalize to Python lists: `[[1,2],[3,4]]`.
   - Capture ALL matrices involved (e.g., A and B).
   - PRESERVE exact numerical values.

3. **INSTRUCTION**: The execution sequence of operations.
   - **Rule 1 (Binary Ops First):** If there are multiple matrices, identifying how they combine (multiply, add) is ALWAYS the first step.
   - **Rule 2 (Inside-Out):** Parse natural language from the innermost operation to the outermost.
     - "Inverse of the Transpose of the Multiplication" -> `multiply then transpose then inverse`
     - "Transpose of A" -> `transpose`
   - **Rule 3 (Format):** Use ' then ' as a separator.
   - **Rule 4 (Keywords):** Normalize to: `inverse`, `transpose`, `multiply`, `add`, `determinant`.
"""

# Field descriptions for Decomposition schema
DECOMPOSE_FORMATTING_DESCRIPTION = (
    "Output format details. E.g., 'latex table', 'latex matrix', 'raw text'. "
    "Default: 'latex matrix'."
)

DECOMPOSE_INSTRUCTION_DESCRIPTION = (
    "Sequence of operations in logical execution order (Inside-Out). "
    "Start with the base operation (like 'multiply' or 'add' for two matrices). "
    "Then apply subsequent operations. "
    "Separator: ' then '. "
    "Example: 'multiply then transpose then inverse'."
)

DECOMPOSE_MATRIX_DESCRIPTION = (
    "String containing all matrix data. "
    "Normalize to Python list-of-lists format e.g., '[[1,2],[3,4]]'. "
    "If multiple matrices, separate clearly or combine in one string."
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
# DSL Verification Prompts (dsl/verifier.py)
# ============================================================================


DSL_VERIFICATION_PROMPT = """

You are a math expert and rigorous code reviewer for a Matrix Operation DSL.
Your goal is to verify if the generated DSL matches the User's intent.

DSL Grammar:
- add(A, B) -> Matrix Addition
- multiply(A, B) -> Matrix Multiplication
- transpose(A) -> Transpose
- inverse(A) -> Inverse

Output Format:
EXPLANATION: [Explain what the DSL does in 1 concise sentence]
MATCH: [TRUE or FALSE]
"""

VERIFY_USER_PROMPT_TEMPLATE = """User Instruction: "{user_instruction}"
Generated DSL: "{dsl_code}"

Task:
1. Explain the DSL logic.
2. Check if it MATCHES the user's instruction (Look out for any kind of misalignment errors!).
3. Return MATCH: TRUE or MATCH: FALSE."""

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


# ============================================================================
# Super-Generator Prompts (One-Pass Architecture)
# ============================================================================

SUPER_GEN_SYSTEM_PROMPT = """
You are a Matrix Operation Expert and DSL Generator.
Your task is to translate the user's natural language request into a valid DSL program.

You have two output channels. You MUST use them in this order:

1. **TEXT CHANNEL (Thought & Format)**: 
   - Analyze the user's request in plain text.
   - Explicitly state the **FORMATTING** requirement (e.g., 'latex table', 'bmatrix', 'raw').
   - Briefly explain the **LOGIC** order (e.g., 'Inside: multiply A, B; Outside: transpose').

2. **TOOL CHANNEL (The Code)**:
   - After your text analysis, generate the executable DSL.
   - **Rule:** Ensure binary operations (multiply, add) are nested correctly w.r.t unary operations (transpose, inverse).
   - **Strictness:** The DSL must strictly follow the provided Lark grammar.

Example Output Flow:
[Text]: "User wants a LaTeX table. Logic is Multiply A & B first, then Inverse."
[Tool]: inverse(multiply([[1,2]], [[3,4]]))
"""

DSL_GENERATOR_TOOL_DESCRIPTION = "Generate the executable matrix DSL code following the Lark grammar."