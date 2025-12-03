# dsl/generator.py
from typing import Optional
from openai import OpenAI
from .grammar import DSL_GRAMMAR
from config.prompts import (
    DSL_GENERATOR_SYSTEM_PROMPT,
    DSL_GENERATOR_FEW_SHOT,
    SUPER_GEN_SYSTEM_PROMPT,
    DSL_GENERATOR_TOOL_DESCRIPTION,
)

def generate_dsl_and_format(client: OpenAI, user_msg: str, *, model: str = "gpt-5") -> dict:
    """
    Super-Generator:
    Uses GPT-5 Responses API to get both reasoning (text) and DSL (constrained tool) in one pass.
    
    Returns:
        dict: {
            "reasoning": str,
            "formatting": str,
            "dsl": str
        }
    """
    user_prompt = f"User Request: {user_msg}"

    # Call GPT-5 Responses API
    resp = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": SUPER_GEN_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        # Configuration: allow both text and custom tool output
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

    # === Parse Dual Outputs ===
    reasoning_text = ""
    formatting_intent = "latex matrix" # Default fallback
    dsl_code = ""

    # Iterate through the output stream
    for item in resp.output:
        # 1. Capture Text Channel (Reasoning & Formatting)
        if hasattr(item, "content") and item.content:
            chunks = []
            for c in item.content:
                if hasattr(c, "text"):
                    chunks.append(c.text)
            
            full_text = "".join(chunks).strip()
            if full_text:
                reasoning_text += full_text + " "
        
        # 2. Capture Tool Channel (DSL) - Constrained by Lark
        if hasattr(item, "input") and isinstance(item.input, str):
            candidate = item.input.strip()
            if candidate:
                dsl_code = candidate

    # NOTE: if dsl is empty string,  it indicates the prompt itself has error
    # the output therefore would be reasoning from gpt-5


    # Simple heuristic to extract formatting intent from reasoning text
    reasoning_lower = reasoning_text.lower()
    if "table" in reasoning_lower:
        formatting_intent = "latex table"
    elif "bmatrix" in reasoning_lower or "matrix" in reasoning_lower:
        formatting_intent = "latex matrix"

    return {
        "reasoning": reasoning_text.strip(),
        "formatting": formatting_intent,
        "dsl": dsl_code 
    }


