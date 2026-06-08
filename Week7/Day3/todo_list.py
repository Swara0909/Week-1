from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END

# State
class State(TypedDict):
    tasks: Annotated[list[str], add]
    query: str
    response: str


# Node
def todo_assistant(state: State):

    query = state["query"]

    if query.lower().startswith("add task:"):
        task = query.split(":", 1)[1].strip()

        return {
            "tasks": [task],
            "response": f"Task '{task}' added!"
        }

    elif query.lower() == "show tasks":

        tasks = state.get("tasks", [])

        if not tasks:
            return {
                "response": "No tasks found."
            }

        task_list = "\n".join(
            [f"{i+1}. {task}" for i, task in enumerate(tasks)]
        )

        return {
            "response": f"Your Tasks:\n{task_list}"
        }

    return {
        "response": "Use 'Add Task: task_name' or 'Show Tasks'"
    }


# Graph
builder = StateGraph(State)

builder.add_node("todo", todo_assistant)

builder.add_edge(START, "todo")
builder.add_edge("todo", END)

graph = builder.compile()


# Memory
tasks_memory = []

while True:

    query = input("\nYou: ")

    if query.lower() == "exit":
        break

    result = graph.invoke({
        "tasks": tasks_memory,
        "query": query
    })

    # Update memory
    if query.lower().startswith("add task:"):
        task = query.split(":", 1)[1].strip()
        tasks_memory.append(task)

    print("\nBot:")
    print(result["response"])