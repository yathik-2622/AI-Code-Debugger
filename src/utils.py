import streamlit as st

def setup_page_config():
    st.set_page_config(
        page_title="AI CODE DEBUGGER & REVIEWER",
        page_icon="🐞",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def render_custom_css():
    st.markdown("""
    <style>
    /* --- APP BACKGROUND --- */
    .stApp { background-color: #0b141a; }

    /* --- USER: ICON LEFT (Standard) --- */
    [data-testid="stChatMessage"]:has(.user-anchor) {
        flex-direction: row !important;
    }
    [data-testid="stChatMessage"]:has(.user-anchor) .stMarkdown {
        background-color: #005c4b !important;
        color: white !important;
        border-radius: 15px;
        border-top-left-radius: 2px;
        width: fit-content !important;
    }

    /* --- BOT: ICON RIGHT (Flipped) --- */
    [data-testid="stChatMessage"]:has(.bot-anchor) {
        flex-direction: row-reverse !important;
    }
    [data-testid="stChatMessage"]:has(.bot-anchor) .stMarkdown {
        background-color: #202c33 !important;
        color: white !important;
        border-radius: 15px;
        border-top-right-radius: 2px;
        width: fit-content !important;
        margin-left: auto; /* Pushes bubble to align with right icon */
    }

    /* Hide the anchor markers */
    .user-anchor, .bot-anchor { display: none; }

    /* --- 🟢 TYPING ANIMATION (New) --- */
    .typing-indicator {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 5px;
    }
    
    .typing-indicator span {
        width: 8px;
        height: 8px;
        background-color: #b0b3b8; /* Light grey dots */
        border-radius: 50%;
        animation: bounce 1.4s infinite ease-in-out both;
    }
    
    .typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
    .typing-indicator span:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes bounce {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1); }
    }
    </style>
    """, unsafe_allow_html=True)