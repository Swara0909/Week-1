from typing import TypedDict
from langgraph.graph import StateGraph, END

# State
class MyState(TypedDict):
    message: str

# Node
def chatbot(state):
    return {
        "message": f"Hello {state['message']}"
    }

# Graph
graph = StateGraph(MyState)

graph.add_node("chatbot", chatbot)

graph.set_entry_point("chatbot")

graph.add_edge("chatbot", END)

app = graph.compile()

result = app.invoke({
    "message": "Swara"
})

print(result)