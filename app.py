import streamlit as st
import textwrap
import time 
from main import run_demo
from utils.mailer import send_feedback_email  # Make sure utils/mailer.py exists

# === 1. Page Configuration ===
st.set_page_config(
    page_title="TexLM",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {display: none;}
        .main-header {font-size: 2.5rem; font-weight: 700; color: #333; text-align: center; margin-bottom: 1rem;}
        .sub-header {font-size: 1.2rem; color: #666; text-align: center; margin-bottom: 2rem;}
        .stCodeBlock {margin-top: 1rem;}
        
        /* Optional: Styling to make the top button blend in more */
        div.stButton > button:first-child {
            border: none;
            background-color: transparent;
            font-size: 1.2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# === Feedback Modal Logic ===
@st.dialog("📋 Report Issue")
def feedback_modal():
    st.markdown("""
    Encountered an edge case or a bug? 
    **Your current chat history will be automatically attached.**
    """)
    
    # Text area for user comments
    user_note = st.text_area(
        "Describe the issue (optional):", 
        placeholder="e.g., The matrix dimension check failed..."
    )
    
    # Send button (Primary action inside modal)
    if st.button("🚀 Send Report", type="primary", key="submit_report"):
        with st.spinner("Sending feedback..."):
            # Call the backend mailer function
            success, msg = send_feedback_email(
                user_note=user_note, 
                chat_history=st.session_state.messages 
            )
            
            if success:
                st.success("Thank you! Report sent.")
                time.sleep(1.5)
                st.rerun()
            else:
                st.error(f"Failed to send: {msg}")

# === 2. Top Layout (Button at Top-Right) ===
# Use columns to push the button to the far right
# Ratio [10, 1] ensures the button stays small and to the right
col_left, col_center, col_right = st.columns([1, 8, 1])

with col_center:
    st.markdown('<div class="main-header">TexLM 🧮</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Natural Language to Overleaf Code</div>', unsafe_allow_html=True)

with col_right:
    st.write("") 
    if st.button("🐞", help="Report Issue"):
        feedback_modal()
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# === 4. Display Chat History ===
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.write(message["content"])
        else:
            # Assistant Response Payload
            payload = message["content"]
            
            # Case 1: Success
            if payload.get("status") == "SUCCESS":
                if "reasoning" in payload:
                    with st.expander("Thinking Process 💭", expanded=False):
                        st.write(payload["reasoning"])
                
                if "final_latex" in payload:
                    st.code(payload["final_latex"], language="latex")
            
            # Case 2: Needs Rephrasing
            elif payload.get("status") == "NEEDS_REPHRASING":
                st.error("🤔 I couldn't generate a valid result after multiple attempts.")
                
                if "error_reason" in payload:
                    st.warning(f"**Issue:** {payload['error_reason']}")
                
                with st.expander("See failed attempt details"):
                    if "reasoning" in payload:
                        st.write("**AI Thought:**", payload["reasoning"])
                    if "failed_dsl" in payload:
                        st.write("**Generated DSL:**")
                        st.code(payload["failed_dsl"], language="python")
                
                st.info("👉 Please try rephrasing your request.")
            
            # Case 3: System Error
            elif payload.get("status") == "ERROR":
                st.error(f"System Error: {payload.get('error')}")

# === 5. Chat Input & Processing ===
if prompt := st.chat_input("Describe your matrix operation..."):
    
    # 1. Append User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # 2. Assistant Message
    with st.chat_message("assistant"):
        import time # ensure time is imported if used
        with st.spinner("🧠 TexLM is thinking and calculating..."):
            try:
                response = run_demo(prompt)
            except Exception as e:
                response = {"status": "ERROR", "error": str(e)}

        # 3. Handle & Display Response
        if response.get("status") == "SUCCESS":
            with st.expander("Thinking Process 💭", expanded=True):
                st.write(response.get("reasoning", ""))
            
            st.code(response["final_latex"], language="latex")
            st.session_state.messages.append({"role": "assistant", "content": response})

        elif response.get("status") == "NEEDS_REPHRASING":
            st.error("🤔 I tried 3 times but couldn't get it right.")
            st.warning(f"**Issue:** {response.get('error_reason')}")
            
            with st.expander("See failed attempt details"):
                st.write("**Generated DSL:**")
                st.code(response.get('failed_dsl'), language="python")

            st.info("👉 Please try rephrasing your prompt or fixing the input numbers.")
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        else:
            st.error(f"System Error: {response.get('error')}")