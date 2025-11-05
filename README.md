# TexLM: Matrix Operations with Natural Language

A modular system that uses LLMs to parse natural language matrix operation requests, generate a domain-specific language (DSL), and render results. Built with OpenAI's Responses API and structured outputs.

## Architecture Overview

The system follows a clean pipeline:

1. **Natural Language Decomposition**  
   Parse user's natural language input into structured components:
   - `formatting`: How the output should be formatted (e.g., "latex table with width = 70%")
   - `instruction`: Matrix operations in clear sequence (e.g., "transpose then inverse")
   - `matrix`: Matrix data normalized to Python list format

2. **DSL Generation**  
   Generate a grammar-constrained DSL program from the instruction and matrix data.  
   The DSL supports operations like `transpose`, `inverse`, `multiply`, `add` with nested compositions.

3. **DSL Execution** (Future)  
   Parse the DSL into AST and execute the matrix operations.

4. **Rendering** (Future)  
   Format the result matrix according to the formatting requirements (e.g., LaTeX table).

---

## Project Structure

```text
TexLM/
├── main.py                    # Entry point: orchestrates the pipeline
├── config/                    # Configuration and prompts
│   ├── __init__.py           # Module exports
│   ├── config.py             # OpenAI client setup, env loading
│   └── prompts.py            # Centralized LLM prompts (all hardcoded prompts here)
├── renderers/                 # LLM-based rendering and decomposition
│   ├── decompose.py          # Natural language → structured Decomposition
│   └── latex.py              # Matrix → LaTeX formatting
├── dsl/                       # Domain-Specific Language
│   ├── grammar.py            # Lark grammar definition for DSL
│   ├── generator.py          # LLM-based DSL generation (grammar-constrained)
│   ├── parser.py             # DSL string → AST (for future execution)
│   └── executor.py           # AST execution (for future implementation)
├── tasks/                     # Task execution (for future use)
│   ├── base.py               # BaseTask abstract class (execute method)
│   └── transpose.py          # Example task implementation
├── requirements.txt          # Python dependencies
├── openai_key.env            # API key (not committed)
└── README.md                  # This file
```

---

## Prerequisites

- Python 3.10+ (3.12 recommended)
- OpenAI API key
- Dependencies: `pip install -r requirements.txt`

Required packages:
- `openai` - OpenAI API client
- `python-dotenv` - Environment variable loading
- `pydantic` - Structured data validation

---

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Create `openai_key.env` in the project root:

```env
OPENAI_API_KEY=sk-your-key-here
```

**Important**: This file is not committed to git. The `config/config.py` loads it automatically.

### 3. Run the Demo

```bash
python main.py
```

Example output:

```text
=== User Message ===
User Message: give me a latex table of the inverse of the transpose of the multiplication of matrix ([1,2] ,[3,4]) and  matrix ([4,5] ,[6,7])

=== Decomposition ===
Formatting: latex table
Instruction: multiply then transpose then inverse
Matrix: [[1,2],[3,4]]; [[4,5],[6,7]]

=== DSL ===
inverse(transpose(multiply([[1,2],[3,4]], [[4,5],[6,7]])))
```

---

## How It Works

### Step 1: Natural Language Decomposition

The system uses an LLM to parse natural language input into structured components:

```python
from renderers.decompose import decompose_user_message

decomp = decompose_user_message(client, user_msg)
# Returns: Decomposition(formatting="latex table", 
#                        instruction="multiply then transpose then inverse",
#                        matrix="[[1,2],[3,4]]; [[4,5],[6,7]]")
```

The LLM is instructed to:
- Extract formatting requirements (defaults to "latex matrix" if unspecified)
- Parse operation sequence correctly (handles natural language like "inverse of transpose")
- Normalize matrix data to Python list format

### Step 2: DSL Generation

The system generates a grammar-constrained DSL program:

```python
from dsl.generator import generate_dsl

dsl = generate_dsl(client, decomp.instruction, decomp.matrix)
# Returns: "inverse(transpose(multiply([[1,2],[3,4]], [[4,5],[6,7]])))"
```

The DSL generator:
- Uses OpenAI's grammar-constrained decoding to ensure valid DSL syntax
- Supports nested operations: `transpose`, `inverse`, `multiply`, `add`
- Handles multiple matrices automatically

### Step 3: DSL Grammar

The DSL is defined by a Lark grammar (see `dsl/grammar.py`):

```
start: call | matrix

call: fname LPAR start RPAR
    | "multiply" LPAR start COMMA SP start RPAR
    | "add"      LPAR start COMMA SP start RPAR

fname: "transpose" | "inverse"

matrix: [[1,2],[3,4]]  # Python list format
```

Valid DSL examples:
- `transpose([[1,2],[3,4]])`
- `inverse(transpose([[1,2],[3,4]]))`
- `multiply([[1,2],[3,4]], [[5,6],[7,8]])`
- `transpose(multiply([[1,0],[2,3]], [[4],[5]]))`

---

## Configuration

### Centralized Prompts

All LLM prompts are centralized in `config/prompts.py` for easy maintenance:

- `DECOMPOSE_SYSTEM_PROMPT` - Instructions for natural language decomposition
- `DSL_GENERATOR_SYSTEM_PROMPT` - Instructions for DSL generation
- `LATEX_RENDER_SYSTEM_PROMPT` - Instructions for LaTeX rendering
- Field descriptions for structured outputs

### Client Configuration

The OpenAI client is configured in `config/config.py`:

```python
from config.config import get_client

client = get_client()  # Returns OpenAI() with API key from env
```

---

## Extending the System

### Adding New Operations

To add a new matrix operation (e.g., `determinant`):

1. **Update the DSL grammar** (`dsl/grammar.py`):
   ```python
   fname: "transpose" | "inverse" | "determinant"
   ```

2. **Update prompts** (`config/prompts.py`):
   - Add examples in `DSL_GENERATOR_FEW_SHOT`
   - Update instruction parsing rules in `DECOMPOSE_INSTRUCTION_DESCRIPTION`

3. **Implement execution** (future):
   - Add executor function in `dsl/executor.py`
   - Update `dsl/parser.py` if needed

### Customizing Prompts

Edit `config/prompts.py` to modify:
- How natural language is parsed
- How DSL is generated
- How results are formatted

All prompts are hardcoded constants for easy maintenance and version control.

---

## Future Work

The current implementation focuses on:
- ✅ Natural language parsing
- ✅ DSL generation with grammar constraints
- 🔄 DSL parsing to AST (parser exists, needs integration)
- 🔄 Matrix operation execution (executor exists, needs integration)
- 🔄 LaTeX rendering (renderer exists, needs integration)

---

## Notes

- **Structured Outputs**: We use OpenAI's `responses.parse()` for reliable structured data extraction
- **Grammar Constraints**: DSL generation uses grammar-constrained decoding to ensure valid syntax
- **Prompt Management**: All prompts are centralized in `config/prompts.py` for easy updates
- **Error Handling**: The system handles ambiguous user input by making clear, specific decisions
- **Modularity**: Each component (decomposition, generation, execution, rendering) is independent

---

## Example Usage

```python
from main import run_demo

user_msg = "give me a latex table of the inverse of the transpose of matrix ([1,2] ,[3,4])"
result = run_demo(user_msg)

print(result["decomposition"])  # Structured parsing result
print(result["dsl"])             # Generated DSL program
```

---

## License

This is a demo project for educational purposes.
