import streamlit as st
import time
from main import run_demo

# === 1. Page Configuration (No Sidebar, Wide Mode) ===
st.set_page_config(
    page_title="TexLM",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS to hide the sidebar completely and style the header
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {display: none;}
        .main-header {font-size: 2.5rem; font-weight: 700; color: #333; text-align: center; margin-bottom: 1rem;}
        .sub-header {font-size: 1.2rem; color: #666; text-align: center; margin-bottom: 2rem;}
    </style>
    """,
    unsafe_allow_html=True
)

# === 2. Header ===
st.markdown('<div class="main-header">TexLM 🧮</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Natural Language to Matrix LaTeX Engine</div>', unsafe_allow_html=True)

# === 3. Session State Management (History) ===
if "messages" not in st.session_state:
    st.session_state.messages = []

# === 4. Display Chat History ===
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # display user input
        if message["role"] == "user":
            st.write(message["content"])
        # display structured model output 
        else:
            payload = message["content"]
            
            # A. Thinking Process (Expandable like Gemini)
            if "reasoning" in payload:
                with st.expander("Thinking Process 💭", expanded=False):
                    st.write(payload["reasoning"])
            
            # B. Rendered Result
            if "final_latex" in payload:
                st.latex(payload["final_latex"])
                
            # C. Copy-pasteable Code Block
            if "final_latex" in payload:
                st.code(payload["final_latex"], language="latex")
                
            # D. Debug Info (Optional - DSL)
            if "dsl" in payload:
                with st.expander("View Generated DSL Code"):
                    st.code(payload["dsl"], language="python")

# === 5. Chat Input & Processing ===
if prompt := st.chat_input("Describe your matrix operation (e.g., 'Inverse of transpose of [[1,2],[3,4]]')..."):
    
    # --- User Step ---
    # 1. Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    # 2. Display user message immediately
    with st.chat_message("user"):
        st.write(prompt)

    # --- Assistant Step ---
    with st.chat_message("assistant"):
        # 1. Loading Indicator (Spinner)
        with st.spinner("🧠 TexLM is thinking and calculating..."):
            try:
                # CALL THE BACKEND
                response_data = run_demo(prompt)
            except Exception as e:
                response_data = None
                st.error(f"System Error: {str(e)}")

        # 2. Display Response
        if response_data and "error" not in response_data:
            # A. Thinking Process
            with st.expander("Thinking Process 💭", expanded=True): # display the thought process
                st.write(response_data.get("reasoning", "No reasoning provided."))
            
            # B. Rendered Latex
            st.latex(response_data["final_latex"])
            
            # C. Code Block
            st.code(response_data["final_latex"], language="latex")
            
            # Save to history
            st.session_state.messages.append({"role": "assistant", "content": response_data})
            
        elif response_data and "error" in response_data:
             st.error(f"Execution Failed: {response_data['error']}")
        else:
             st.warning("Sorry, I couldn't understand that request. Please try again.")