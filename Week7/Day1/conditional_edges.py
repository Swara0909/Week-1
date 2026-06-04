from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    score: int

def check_score(state):
    return state

def pass_node(state):
    print("Passed")
    return state

def fail_node(state):
    print("Failed")
    return state

def route(state):
    if state["score"] >= 50:
        return "pass"
    return "fail"

graph = StateGraph(State)

graph.add_node("check", check_score)
graph.add_node("pass", pass_node)
graph.add_node("fail", fail_node)

graph.add_edge(START, "check")

graph.add_conditional_edges(
    "check",
    route,
    {
        "pass": "pass",
        "fail": "fail"
    }
)

graph.add_edge("pass", END)
graph.add_edge("fail", END)

app = graph.compile()

app.invoke({"score": 80})