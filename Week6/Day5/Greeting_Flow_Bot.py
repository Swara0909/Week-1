from typing import TypedDict

class State(TypedDict):
    name: str
    greeting: str

def clean_name(state: State):
    cleaned = state["name"].title().strip()

    return {
        "name": cleaned
    }

def generate_greeting(state: State):
    return {
        "greeting": f"Hello {state['name']}, welcome to AI Lab!"
    }

from langgraph.graph import StateGraph, START, END

builder = StateGraph(State)

builder.add_node("clean_name", clean_name)
builder.add_node("generate_greeting", generate_greeting)

builder.add_edge(START, "clean_name")
builder.add_edge("clean_name", "generate_greeting")
builder.add_edge("generate_greeting", END)

graph = builder.compile()   

result = graph.invoke({
    "name": "john smith"
})

print(result["greeting"])