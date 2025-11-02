# Matrix-DSL LLM Demo

This repo is a small, modular demo that shows how to use OpenAI's **Responses API** together with a tiny matrix DSL.

The idea is:

1. **LLM #1 – decomposition**  
   We send the raw user message to the LLM and ask it to *structure* it.  
   The model must return:
   - `matrix_data`: the matrix the user mentioned (normalized to something like `[[1,2],[3,4]]`)
   - `task_name`: which operation to run, e.g. `transpose`, `matmul`, `add`
   - `task_args` (optional): extra parameters for the task
   - `render_task`: how the user wants to see the result (e.g. “in LaTeX”)

2. **Task routing**  
   Based on `task_name` we look up a corresponding Task class (see `task_registry.py`).  
   Each Task knows how to:
   - build a concrete DSL string (e.g. `transpose((2, 3, float), (3, 2, float))`)
   - execute it (check shapes, run Python, return the new matrix)

3. **DSL layer**  
   The DSL is intentionally tiny. For now it supports (at least) `transpose`.  
   Parsing happens in `dsl/parser.py`, execution in `dsl/executor.py`.  
   This makes it easy to add more matrix ops without changing the main script.

4. **LLM #3 – rendering**  
   After executing the matrix operation, we ask the LLM to render the result in LaTeX  
   (see `renderers/latex.py`). This keeps formatting concerns out of the DSL.

---

## Project layout

```text
project/
├── main.py              # entry point: glue everything together
├── config.py            # loads env, creates OpenAI client
├── schemas.py           # pydantic models for LLM structured output
├── llm_decompose.py     # LLM #1: user message -> structured Decomposition
├── task_registry.py     # maps task_name -> concrete Task class
├── tasks/
│   ├── __init__.py
│   ├── base.py          # BaseTask: every task must implement build_dsl + execute
│   └── transpose.py     # example task, currently supported
├── dsl/
│   ├── __init__.py
│   ├── parser.py        # turns DSL string into a small AST/dict
│   └── executor.py      # actually runs the operation in Python
├── renderers/
│   ├── __init__.py
│   └── latex.py         # LLM #3: matrix -> LaTeX
└── openai_key.env       # NOT committed, contains OPENAI_API_KEY
```

---

## Prerequisites

- Python 3.10+ (3.12 is fine)
- `pip install -r requirements.txt` (at least `openai`, `python-dotenv`, `pydantic`)
- An OpenAI API key

---

## Environment setup

Create a file called **`openai_key.env`** in the project root:

```env
OPENAI_API_KEY=sk-your-key-here
```

We deliberately **do not** commit this file (see `.gitignore` below).

In `config.py` we load it with:

```python
from dotenv import load_dotenv
load_dotenv("openai_key.env")
```

Then we create the client:

```python
from openai import OpenAI
client = OpenAI()
```

Because the key is already in the environment, we don’t have to pass it manually.

---

## Running the demo

From the project directory:

```bash
python main.py
```

You should see output like:

```text
=== decomposition ===
{'matrix_data': '[[1,2],[3,4]]', 'task_name': 'transpose', 'render_task': 'in LaTeX', ...}
=== DSL ===
transpose((2, 2, float), (2, 2, float))
=== result ===
[[1, 3], [2, 4]]
=== LaTeX ===
\begin{bmatrix}
...
\end{bmatrix}
```

(Exact output depends on the model.)

---

## Adding a new task

1. Create a new file in `tasks/`, e.g. `tasks/matmul.py`.
2. Inherit from `BaseTask` and implement:
   - `build_dsl(...)`
   - `execute(...)`
3. Register it in `task_registry.py`:

   ```python
   from tasks.matmul import MatmulTask

   TASK_REGISTRY = {
       "transpose": TransposeTask,
       "matmul": MatmulTask,
   }
   ```

4. Update the system prompt in `llm_decompose.py` to include `"matmul"` in the allowed task names so the LLM can pick it.

That’s it — you don’t have to touch `main.py`.

---

## Notes

- We use *structured outputs* (`client.responses.parse(...)`) so that the LLM returns data we can feed directly into Python/Pydantic.
- If you start getting schema errors from the API, check `schemas.py` first — structured outputs are strict about the JSON shape.
- This repo is just a demo; in a real system you would also log all raw LLM responses for debugging.
