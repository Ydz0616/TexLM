import streamlit as st
import textwrap
from main import run_demo

# === 1. Page Configuration ===
st.set_page_config(
    page_title="TexLM",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for a clean look
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {display: none;}
        .main-header {font-size: 2.5rem; font-weight: 700; color: #333; text-align: center; margin-bottom: 1rem;}
        .sub-header {font-size: 1.2rem; color: #666; text-align: center; margin-bottom: 2rem;}
        .stCodeBlock {margin-top: 1rem;}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-header">TexLM 🧮</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Natural Language to Overleaf Code</div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# === 2. Display Chat History ===
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.write(message["content"])
        else:
            # Assistant Response
            payload = message["content"]
            
            # A. Thinking Process
            if "reasoning" in payload:
                with st.expander("Thinking Process 💭", expanded=False):
                    st.write(payload["reasoning"])
            
            # B. LaTeX Code Block (Directly for Overleaf)
            if "final_latex" in payload:
                st.code(payload["final_latex"], language="latex")

# === 3. Chat Input & Processing ===
if prompt := st.chat_input("Describe your matrix operation..."):
    # User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Assistant Message
    with st.chat_message("assistant"):
        with st.spinner("🧠 TexLM is generating code..."):
            try:
                response_data = run_demo(prompt)
            except Exception as e:
                response_data = None
                st.error(f"System Error: {str(e)}")

        if response_data and "error" not in response_data:
            # A. Thinking Process (Default Expanded)
            with st.expander("Thinking Process 💭", expanded=True):
                st.write(response_data.get("reasoning", "No reasoning provided."))
            
            # B. LaTeX Code (No rendering, just code)
            st.code(response_data["final_latex"], language="latex")
            
            # Save to history
            st.session_state.messages.append({"role": "assistant", "content": response_data})
            
        elif response_data and "error" in response_data:
             st.error(f"Execution Failed: {response_data['error']}")
        else:
             st.warning("Sorry, I couldn't understand that request.")