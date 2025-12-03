# utils/mailer.py
import smtplib
import os
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_feedback_email(user_note: str, chat_history: list) -> tuple[bool, str]:
    """
    Sends an email to the administrator via Gmail SMTP with user feedback and chat logs.
    
    Args:
        user_note (str): The feedback message entered by the user.
        chat_history (list): The full session state messages to attach as a log.
        
    Returns:
        tuple: (bool success, str message)
    """
    # 1. Retrieve credentials from environment variables
    # For local testing, ensure these are set in your terminal or .env file
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")
    # You can change this to a specific admin email if different from sender
    receiver_email = sender_email 

    if not sender_email or not sender_password:
        return False, "Server email configuration is missing (EMAIL_USER or EMAIL_PASS)."

    # 2. Serialize chat history to JSON
    try:
        history_dump = json.dumps(chat_history, indent=2, ensure_ascii=False)
    except Exception as e:
        history_dump = f"Failed to serialize history: {str(e)}"

    # 3. Construct the Email Message
    msg = MIMEMultipart()
    msg['From'] = f"TexLM Bot <{sender_email}>"
    msg['To'] = receiver_email
    msg['Subject'] = "[TexLM Feedback] User Report"

    # Email body content (HTML)
    body = f"""
    <h3>User Feedback Report</h3>
    <p><strong>User Note:</strong><br>{user_note}</p>
    <hr>
    <h4>Session Logs (JSON)</h4>
    <pre style="background-color: #f4f4f4; padding: 10px; border-radius: 5px;">{history_dump}</pre>
    """
    msg.attach(MIMEText(body, 'html'))

    # 4. Send via Gmail SMTP
    try:
        # Gmail SMTP configuration: smtp.gmail.com, port 587
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Upgrade connection to secure TLS encryption
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True, "Feedback sent successfully!"
        
    except smtplib.SMTPAuthenticationError:
        return False, "Authentication failed. Check your Gmail App Password."
    except Exception as e:
        return False, f"SMTP Error: {str(e)}"