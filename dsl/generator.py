# dsl/generator.py
from typing import Optional
from openai import OpenAI
from .grammar import DSL_GRAMMAR
from config.prompts import (
    DSL_GENERATOR_SYSTEM_PROMPT,
    DSL_GENERATOR_FEW_SHOT,
    DSL_GENERATOR_TOOL_DESCRIPTION,
)

def _build_user_prompt(instruction: str, matrix_text: str) -> str:
    """
    matrix_text: String, e.g., '[[1,2],[3,4]]' or 'A=[[...]]; B=[[...]]'
    Multiple matrices can be joined with ';' or described in the instruction.
    """
    return (
        f"{DSL_GENERATOR_FEW_SHOT}\n"
        f"User: instruction={instruction}; matrix={matrix_text}\n"
        f"DSL:"
    )

def generate_dsl(client: OpenAI, instruction: str, matrix_text: str, *, model: str = "gpt-5") -> str:
    prompt = _build_user_prompt(instruction, matrix_text)

    resp = client.responses.create(
        model=model,
        input=[{"role": "system", "content": DSL_GENERATOR_SYSTEM_PROMPT},
               {"role": "user", "content": prompt}],
        text={"format": {"type": "text"}, "verbosity": "low"},
        reasoning={"effort": "minimal"},
        tools=[{
            "type": "custom",
            "name": "dsl_grammar",
            "description": DSL_GENERATOR_TOOL_DESCRIPTION,
            "format": {
                "type": "grammar",
                "syntax": "lark",
                "definition": DSL_GRAMMAR
            }
        }],
        parallel_tool_calls=False
    )

    # Output from constrained decoding (preferred path)
    try:
        return resp.output[1].input.strip()
    except Exception:
        # Fallback: if the model emitted the DSL as plain text content instead of a tool call
        chunks = []
        for item in resp.output:
            if hasattr(item, "content") and item.content:
                for c in item.content:
                    if hasattr(c, "text"):
                        chunks.append(c.text)
        return "".join(chunks).strip()
