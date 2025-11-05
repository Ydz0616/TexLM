# renderers/decompose.py
from pydantic import BaseModel, Field
from openai import OpenAI
from config.prompts import (
    DECOMPOSE_SYSTEM_PROMPT,
    DECOMPOSE_FORMATTING_DESCRIPTION,
    DECOMPOSE_INSTRUCTION_DESCRIPTION,
    DECOMPOSE_MATRIX_DESCRIPTION,
)

class Decomposition(BaseModel):
    """
    Decomposition of user's natural language input into structured components.
    All fields must be clear and unambiguous, even if user's description is vague.
    """
    formatting: str = Field(description=DECOMPOSE_FORMATTING_DESCRIPTION)
    
    instruction: str = Field(description=DECOMPOSE_INSTRUCTION_DESCRIPTION)
    
    matrix: str = Field(description=DECOMPOSE_MATRIX_DESCRIPTION)

def decompose_user_message(client: OpenAI, user_msg: str, *, model: str = "gpt-4o-mini") -> Decomposition:
    """
    Parse natural language input into structured components.
    
    Args:
        client: OpenAI client
        user_msg: Natural language input from user
        model: Model to use for parsing (default: gpt-4o-mini)
    
    Returns:
        Decomposition object with formatting, instruction, and matrix fields
    """
    resp = client.responses.parse(
        model=model,
        input=[
            {"role": "system", "content": DECOMPOSE_SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        text_format=Decomposition,
    )
    return resp.output_parsed

