from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# State Schema
class State(TypedDict):
    query: str
    response: str


# Greeting Node
def greeting(state: State):
    return {
        "response": "Hello! Welcome to AI Labs!"
    }


# Math Node
def math_node(state: State):
    query = state["query"]

    try:
        result = eval(query)
        return {
            "response": f"Result = {result}"
        }
    except Exception:
        return {
            "response": "Invalid mathematical expression"
        }


# General Query Node
def general_query(state: State):
    return {
        "response": f"You asked: {state['query']}"
    }


# Router Function
def router(state: State):
    query = state["query"].lower().strip()

    # Greeting Intent
    if query in ["hello", "hi", "hey"]:
        return "greeting"

    # Math Intent
    elif any(op in query for op in ["+", "-", "*", "/"]):
        return "math"

    # General Intent
    else:
        return "general"


# Build Graph
builder = StateGraph(State)

builder.add_node("greeting", greeting)
builder.add_node("math", math_node)
builder.add_node("general", general_query)

builder.add_conditional_edges(
    START,
    router,
    {
        "greeting": "greeting",
        "math": "math",
        "general": "general"
    }
)

builder.add_edge("greeting", END)
builder.add_edge("math", END)
builder.add_edge("general", END)

graph = builder.compile()

user_input = input("Enter your query")
result = graph.invoke({
    "query": user_input,
    "response": ""
})

print(result["response"])