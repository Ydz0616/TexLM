# utils/mailer.py
import smtplib
import os
import json
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv, find_dotenv

# === Load Environment Variables ===
current_dir = Path(__file__).parent
project_root = current_dir.parent
env_candidates = [
    project_root / "openai_key.env",
    project_root / "openai.env",
]

def _load_env_file() -> Path:
    for candidate in env_candidates:
        if candidate.exists():
            load_dotenv(candidate, override=False)
            return candidate
    found = find_dotenv()
    if found:
        load_dotenv(found, override=False)
        return Path(found)
    load_dotenv(env_candidates[0], override=False)
    return env_candidates[0]

env_path = _load_env_file()

def _clean_env_var(val: str | None) -> str | None:
    """
        Strip common whitespace artifacts (including non-breaking spaces)
        that often sneak into copied env files.
    """
    if val is None:
        return None
    return val.strip().replace("\u00a0", "").replace(" ", "")


def send_feedback_email(user_note: str, chat_history: list) -> tuple[bool, str]:
    """
    Sends an email to the administrator via Gmail SMTP.
    """
    # 1. Retrieve credentials
    sender_email = _clean_env_var(os.getenv("EMAIL_USER"))
    sender_password = _clean_env_var(os.getenv("EMAIL_PASS"))
    
    receiver_email = sender_email 

    if not sender_email or not sender_password:
        return False, f"Missing email config in {env_path.name}. Please check EMAIL_USER and EMAIL_PASS."

    # 2. Prepare Data (JSON Dump)
    try:
        history_dump = json.dumps(chat_history, indent=2, ensure_ascii=False)
    except Exception as e:
        history_dump = f"Serialization Error: {str(e)}"

    # 3. Build Email
    msg = MIMEMultipart()
    msg['From'] = f"TexLM Bot <{sender_email}>"
    msg['To'] = receiver_email
    msg['Subject'] = "[TexLM Feedback] User Report"

    body = f"""
    <h3>User Feedback Report</h3>
    <p><strong>User Note:</strong><br>{user_note}</p>
    <hr>
    <h4>Session Logs (JSON)</h4>
    <pre style="background-color: #f4f4f4; padding: 10px; border-radius: 5px; white-space: pre-wrap;">{history_dump}</pre>
    """
    
    # utf-8 encoding
    msg.attach(MIMEText(body, 'html', 'utf-8'))

    # 4. Send via Gmail SMTP
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True, "Feedback sent successfully!"
        
    except smtplib.SMTPAuthenticationError:
        return False, "Authentication failed. Please check your App Password."
    except Exception as e:
        return False, f"SMTP Error: {str(e)}"