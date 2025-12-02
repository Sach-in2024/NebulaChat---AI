import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid
import pickle
import os

# ---------------------- UTIL FUNCTIONS ----------------------

def generate_thread_id():
    return str(uuid.uuid4())

def get_chat_title(messages):
    if not messages:
        return "New Chat"
    first_msg = messages[0]['content'].strip()
    return (first_msg[:20] + "...") if len(first_msg) > 20 else first_msg

def load_conversation(thread_id):
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    values = state.values.get("messages", [])
    converted = []
    for msg in values:
        role = "user" if msg.type == "human" else "assistant"
        converted.append({"role": role, "content": msg.content})
    return converted

# ---------------------- DATABASE SIMULATION ----------------------
# Store all threads persistently using pickle
DB_FILE = "chat_threads.pkl"

def save_threads(all_chats):
    with open(DB_FILE, "wb") as f:
        pickle.dump(all_chats, f)

def retrieve_all_threads():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "rb") as f:
            return pickle.load(f)
    return {}

# ---------------------- SESSION SETUP ----------------------

if "message_history" not in st.session_state:
    st.session_state.message_history = []

if "current_chat" not in st.session_state:
    st.session_state.current_chat = generate_thread_id()

if "all_chats" not in st.session_state:
    st.session_state.all_chats = retrieve_all_threads()

# Ensure current chat exists in all_chats
if st.session_state.current_chat not in st.session_state.all_chats:
    st.session_state.all_chats[st.session_state.current_chat] = []

# ---------------------- PAGE UI ----------------------

st.set_page_config(
    page_title="NebulaChat – AI Chatbot",
    page_icon="💬",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1e1e2f, #12121c);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align:center;color:white;'>💬 NebulaChat AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#bbb;'>Your personal intelligent assistant</p>", unsafe_allow_html=True)

# ---------------------- SIDEBAR ----------------------

st.sidebar.title("My Conversations")

# New chat button
if st.sidebar.button("➕ New Chat", key="new_chat_button"):
    new_id = generate_thread_id()
    st.session_state.current_chat = new_id
    st.session_state.message_history = []
    st.session_state.all_chats[new_id] = []
    save_threads(st.session_state.all_chats)

# List chats with unique keys
for i, (thread_id, msgs) in enumerate(st.session_state.all_chats.items()):
    title = get_chat_title(msgs)
    if st.sidebar.button(title, key=f"chat_{i}"):
        st.session_state.current_chat = thread_id
        st.session_state.message_history = load_conversation(thread_id)
        st.session_state.all_chats[thread_id] = st.session_state.message_history
        save_threads(st.session_state.all_chats)

# ---------------------- CHAT HISTORY ----------------------

for message in st.session_state.message_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------- USER INPUT ----------------------

user_input = st.chat_input("Type your message...")

if user_input:
    # store user message
    st.session_state.message_history.append({"role": "user", "content": user_input})
    st.session_state.all_chats[st.session_state.current_chat] = st.session_state.message_history
    save_threads(st.session_state.all_chats)

    with st.chat_message("user"):
        st.markdown(user_input)

    # invoke backend with thread_id
    response = chatbot.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config={"configurable": {"thread_id": st.session_state.current_chat}}
    )

    ai_msg = response["messages"][-1].content

    # store ai response
    st.session_state.message_history.append({"role": "assistant", "content": ai_msg})
    st.session_state.all_chats[st.session_state.current_chat] = st.session_state.message_history
    save_threads(st.session_state.all_chats)

    with st.chat_message("assistant"):
        st.markdown(ai_msg)
