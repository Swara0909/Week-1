from typing import TypedDict, Annotated
from operator import add

from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage

from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

# Load API key
load_dotenv("../.env")

hf_token = os.getenv("HF_TOKEN")

# Hugging Face Client
client = InferenceClient(
    api_key=hf_token
)

# State
class State(TypedDict):
    messages: Annotated[list, add]


# Chatbot Node
def chatbot(state: State):

    messages = []

    for msg in state["messages"]:
        messages.append({
            "role": "user",
            "content": msg.content
        })

    response = client.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=messages,
        max_tokens=200
    )

    answer = response.choices[0].message.content

    return {
        "messages": [
            AIMessage(content=answer)
        ]
    }


# Build Graph
builder = StateGraph(State)

builder.add_node("chatbot", chatbot)

builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

graph = builder.compile()


# Memory
user_memory = []

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    user_memory.append(user_input)

    # Remember only last 3 messages
    recent_messages = user_memory[-3:]

    context = [
        HumanMessage(content=msg)
        for msg in recent_messages
    ]

    result = graph.invoke({
        "messages": context
    })

    print("Bot:", result["messages"][-1].content)