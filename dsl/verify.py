from openai import OpenAI
from config.prompts import DSL_VERIFICATION_PROMPT, VERIFY_USER_PROMPT_TEMPLATE

def verify(client: OpenAI, model:str, user_instruction:str,dsl_code:str) -> dict:
    user_prompt = VERIFY_USER_PROMPT_TEMPLATE.format(
        user_instruction=user_instruction,
        dsl_code=dsl_code
    )

    resp = client.chat.completions.create(
        model = model,
        messages = [
            {
                "role": "system",
                "content": DSL_VERIFICATION_PROMPT
            },
            {
                "role":"user",
                "content": user_prompt
            }
        ]
    )
    content = resp.choices[0].message.content
    
    is_match = "MATCH: TRUE" in content
    explanation = "N/A"
    if "EXPLANATION:" in content:
        explanation = content.split("EXPLANATION:")[1].split("MATCH:")[0].strip()
    
    return {
        "is_valid": is_match,
        "explanation": explanation,
        "raw": content
    }


