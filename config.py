# config.py
import os
from dotenv import load_dotenv
from openai import OpenAI

# i got 5 bucks in it lol
load_dotenv("openai_key.env")

def get_client() -> OpenAI:
    
    return OpenAI()


