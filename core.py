from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()
model = os.environ.get('GROQ_MODEL')
llm = ChatGroq(model_name=model)

# Load profile text
base_dir = os.path.dirname(os.path.abspath(__file__))
profile_path = os.path.join(base_dir, 'profile.txt')

if os.path.exists(profile_path):
    with open(profile_path, 'r', encoding='utf-8') as f:
        profile_text = f.read()
else:
    profile_text = "No profile found."

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    parser = StrOutputParser()

# Prompt template
    chat_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful and conversational AI assistant. Answer user questions confidently and directly based on Aiswarya Baby’s profile below. If asked whether something was created by her, and the profile confirms it, clearly say 'yes' in your reply. Provide short, friendly, and informative answers. when user says bye or exit, say nice chatting with you\n\n{profile}"),
        ("human", "{input}")
    ])
    chain = chat_template | llm | parser
    response = chain.invoke({
                    "profile": profile_text,
                    "input": messages
                })
    return {"messages": [response]}

# Checkpointer
checkpointer = InMemorySaver()

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)