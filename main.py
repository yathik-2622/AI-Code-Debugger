import streamlit as st
import time
from src.utils import setup_page_config, render_custom_css
from src.llm_engine import CodeAnalysisEngine

# 1. SETUP
setup_page_config()
render_custom_css()

if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. SIDEBAR
with st.sidebar:
    st.header("⚙️ Settings")
    language = st.selectbox("Language", ["Python", "Java", "C++", "JavaScript", "SQL"])
    st.markdown("---")
    st.caption("Mode: **Production Debugger**")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 3. HEADER
st.title("⚝ AI Code Architect")
st.caption("Automated Logic Analysis & Optimization")

# 4. CHAT HISTORY
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar="⚡"):
            st.markdown(msg["content"])

# 5. INPUT & LOGIC
if prompt := st.chat_input("Paste code to Analyse & Review..."):
    
    # Render User (Right)
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Render Bot (Left)
    with st.chat_message("assistant", avatar="⚡"):
        try:
            # --- 1. LOADING ANIMATION (Replaces logs) ---
            message_placeholder = st.empty()
            
            # Show Bouncing Dots while processing
            message_placeholder.markdown("""
                <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            """, unsafe_allow_html=True)
            
            # --- 2. PROCESSING ---
            engine = CodeAnalysisEngine()
            
            # Short delay to make the animation feel natural
            time.sleep(1.0) 
            
            # Retrieve RAG context silently
            context = engine.get_context(prompt)
            
            # --- 3. STREAM RESPONSE ---
            # Remove the dots
            message_placeholder.empty()
            
            # Stream the text
            response_stream = engine.stream_analysis(prompt, language, context)
            full_response = st.write_stream(response_stream)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Error: {e}")