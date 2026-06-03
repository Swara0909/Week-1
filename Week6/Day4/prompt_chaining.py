from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    topic: str
    outline: str
    blog: str

# Node 1
def generate_topic(state):
    return {"topic": "Artificial Intelligence"}

# Node 2
def generate_outline(state):
    topic = state["topic"]
    return {
        "outline": f"""
        1. Introduction to {topic}
        2. Applications
        3. Benefits
        4. Challenges
        """
    }

# Node 3
def generate_blog(state):
    outline = state["outline"]
    return {
        "blog": f"Blog generated from:\n{outline}"
    }

builder = StateGraph(State)

builder.add_node("topic", generate_topic)
builder.add_node("outline", generate_outline)
builder.add_node("blog", generate_blog)

builder.add_edge(START, "topic")
builder.add_edge("topic", "outline")
builder.add_edge("outline", "blog")
builder.add_edge("blog", END)

graph = builder.compile()

result = graph.invoke({})
print(result)