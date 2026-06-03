from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    number:int

def add_five(State):
    return {"number":State["number"]+5}

def multiply_two(State):
    return {"number":State["number"]*2}

builder=StateGraph(State)

builder.add_node(add_five, add_five)
builder.add_node(multiply_two, multiply_two)

builder.add_edge(START, "add_five")
builder.add_edge("add_five", "multiply_two")
builder.add_edge("multiply_two", END)

graph=builder.compile()

result=graph.invoke({"number":10})
print(result)
