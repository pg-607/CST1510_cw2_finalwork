import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
# Page configuration 
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)
load_dotenv()  # Load .env file
def initialize_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "role" not in st.session_state:
        st.session_state.role = ""
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
# Initialize OpenAI client
try:
    # Try environment variable first, then Streamlit secrets, then .env file
    api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
    if not api_key:
        st.error("API key not configured. Set OPENAI_API_KEY environment variable or add to .streamlit/secrets.toml")
        st.stop()
    client = OpenAI(api_key=api_key)
except Exception as e:
    st.error(f"Failed to initialize OpenAI client: {e}")
    st.stop()


st.title("🤖 AI Assistant")
st.caption("Powered by GPT-4o")

# Domain selection 
st.subheader("Select Domain")

domain = st.selectbox(
    "Choose expertise area",
    ["General", "Cybersecurity", "Data Science", "IT Operations"],
    index=0
)

# System prompts for different domains
if domain == "Cybersecurity":
    system_prompt = """You are a cybersecurity expert assistant.
Analyze incidents, threats, and provide technical guidance."""
elif domain == "Data Science":
    system_prompt = """You are a data science expert assistant.
Help with analysis, visualization, and statistical insights."""
elif domain == "IT Operations":
    system_prompt = """You are an IT operations expert assistant.
Help troubleshoot issues, optimize systems, and manage tickets."""
else:
    system_prompt = "You are a helpful assistant."

# Initialize session state 
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]
else:
    # Update system prompt if domain changed
    if len(st.session_state.messages) > 0 and st.session_state.messages[0]["role"] == "system":
        st.session_state.messages[0]["content"] = system_prompt

# Sidebar controls 
with st.sidebar:
    st.subheader("Controls")
    
    # Model selection 
    model = st.selectbox(
        "Model",
        ["gpt-4o-mini", "gpt-4o"],
        index=0
    )
    
    # Temperature 
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=1.0,
        step=0.1,
        help="Higher values make output more random"
    )
    
    # Clear chat 
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = [
            {"role": "system", "content": system_prompt}
        ]
        st.rerun()
    
    # Message count
    user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
    st.metric("Messages", user_messages)

# Display chat history
for message in st.session_state.messages:
    if message["role"] != "system":  # Don't show system prompt (Page 20)
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Get user input 
prompt = st.chat_input(f"Ask about {domain.lower()}...")

if prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add to session state 
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    
    # Call API with 
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."): 
            # Enable streaming 
            completion = client.chat.completions.create(
                model=model,
                messages=st.session_state.messages,
                temperature=temperature,
                stream=True  
            )
            
            # Display streaming response 
            container = st.empty()
            full_reply = ""
            
            for chunk in completion: 
                delta = chunk.choices[0].delta
                if delta.content:  
                    full_reply += delta.content
                    container.markdown(full_reply + "▌") 
            
            container.markdown(full_reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": full_reply
    })

# Navigation
st.markdown("---")
if st.button("Back to Dashboard"):
    st.switch_page("pages/1_Dashboard.py")