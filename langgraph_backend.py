from langgraph.graph import StateGraph
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

checkpointer = InMemorySaver()

# ❗ NEW SYNTAX — no START and END now
graph = StateGraph(ChatState)

graph.add_node("chat", chat_node)

graph.set_entry_point("chat")
graph.set_finish_point("chat")

chatbot = graph.compile(checkpointer=checkpointer)
