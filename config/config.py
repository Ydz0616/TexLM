# config/config.py
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# i got 5 bucks in it lol
# Load from parent directory since config/ is now a subdirectory
config_dir = Path(__file__).parent
project_root = config_dir.parent
load_dotenv(project_root / "openai_key.env")

def get_client() -> OpenAI:
    
    return OpenAI()

