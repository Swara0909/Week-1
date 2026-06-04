from typing import TypedDict, Annotated
from operator import add

from langgraph.graph import StateGraph, START, END

# State
class State(TypedDict):
    messages: Annotated[list[str], add]  # Reducer
    # this stores the values of str in a list and adds whenever a new string comes 

# Nodes
def node1(state):
    return {"messages": ["Hello"]}

def node2(state):
    return {"messages": ["Swara"]}

def node3(state):
    return {"messages": ["Hii"]}

# Graph
builder = StateGraph(State)

builder.add_node("node1", node1)
builder.add_node("node2", node2)
builder.add_node("node3", node3)

builder.add_edge(START, "node1")
builder.add_edge("node1", "node2")
builder.add_edge("node2", "node3")
builder.add_edge("node3", END)

graph = builder.compile()

result = graph.invoke({"messages": []})
print(result)