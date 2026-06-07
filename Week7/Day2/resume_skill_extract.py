from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# State
class State(TypedDict):
    query: str
    response: str


# Python Tool
def python_tool(state: State):
    concepts = {
        "numpy": "NumPy is a Python library for numerical computing and arrays.",
        "pandas": "Pandas is a Python library for data analysis and manipulation.",
        "flask": "Flask is a lightweight Python web framework.",
        "django": "Django is a high-level Python web framework.",
        "tkinter": "Tkinter is Python's standard GUI library."
    }

    query = state["query"].lower()

    for key, value in concepts.items():
        if key in query:
            return {"response": value}

    return {"response": "Python concept not found."}


# MERN Tool
def mern_tool(state: State):
    concepts = {
        "mongodb": "MongoDB is a NoSQL database.",
        "express": "Express.js is a backend framework for Node.js.",
        "react": "React is a JavaScript library for building user interfaces.",
        "node": "Node.js allows JavaScript to run outside the browser."
    }

    query = state["query"].lower()

    for key, value in concepts.items():
        if key in query:
            return {"response": value}

    return {"response": "MERN concept not found."}


# AWS Tool
def aws_tool(state: State):
    concepts = {
        "ec2": "Amazon EC2 provides virtual servers in the cloud.",
        "s3": "Amazon S3 is an object storage service.",
        "lambda": "AWS Lambda runs code without managing servers.",
        "rds": "Amazon RDS is a managed relational database service."
    }

    query = state["query"].lower()

    for key, value in concepts.items():
        if key in query:
            return {"response": value}

    return {"response": "AWS concept not found."}


# Router
def router(state: State):
    query = state["query"].lower()

    if any(word in query for word in
           ["numpy", "pandas", "flask", "django", "tkinter"]):
        return "python"

    elif any(word in query for word in
             ["mongodb", "express", "react", "node"]):
        return "mern"

    elif any(word in query for word in
             ["ec2", "s3", "lambda", "rds"]):
        return "aws"

    return "python"


# Build Graph
builder = StateGraph(State)

builder.add_node("python", python_tool)
builder.add_node("mern", mern_tool)
builder.add_node("aws", aws_tool)

builder.add_conditional_edges(
    START,
    router,
    {
        "python": "python",
        "mern": "mern",
        "aws": "aws"
    }
)

builder.add_edge("python", END)
builder.add_edge("mern", END)
builder.add_edge("aws", END)

graph = builder.compile()

# Test
query = input("Ask a question: ")

result = graph.invoke({
    "query": query
})

print("\nAnswer:")
print(result["response"])