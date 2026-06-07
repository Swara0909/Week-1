from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from datetime import datetime

class State(TypedDict):
    query: str
    response: str

# Tools
def calculator_tool(state: State):
    expression = state["query"].replace("×", "*")
    result = eval(expression)
    return {"response": str(result)}

def date_tool(state: State):
    return {
        "response": datetime.now().strftime("%d-%m-%Y")
    }

def knowledge_tool(state: State):

    kb = {
        "what is ai":
        "Artificial Intelligence is the simulation of human intelligence by machines.",
        "ai": "Artificial Intelligence is the simulation of human intelligence by machines.",
        "python": "Python is a high-level, interpreted programming language.",
        "machine learning": "Machine Learning enables systems to learn from data without explicit programming.",
        "langgraph": "LangGraph is a framework for building stateful AI agent workflows.",
        "llm": "LLM stands for Large Language Model."
    }

    return {
        "response": kb.get(
            state["query"].lower(),
            "Knowledge not found."
        )
    }

# Router
def router(state: State):

    query = state["query"].lower()

    if any(op in query for op in ['+', '-', '*', '/', '×']):
        return "calculator"

    elif "date" in query or "today" in query:
        return "date"

    else:
        return "knowledge"

# Graph
graph_builder = StateGraph(State)

graph_builder.add_node("calculator", calculator_tool)
graph_builder.add_node("date", date_tool)
graph_builder.add_node("knowledge", knowledge_tool)

graph_builder.add_conditional_edges(
    START,
    router,
    {
        "calculator": "calculator",
        "date": "date",
        "knowledge": "knowledge"
    }
)

graph_builder.add_edge("calculator", END)
graph_builder.add_edge("date", END)
graph_builder.add_edge("knowledge", END)

graph = graph_builder.compile()

result = graph.invoke({
    "query": "What is today's date?"
})

print(result["response"])