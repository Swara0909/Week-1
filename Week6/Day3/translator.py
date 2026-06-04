from typing import TypedDict, Annotated

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from langchain_core.messages import HumanMessage, AIMessage
from langchain_ollama import ChatOllama


# ==========================================
# LLM
# ==========================================

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


# ==========================================
# State
# ==========================================

class GraphState(TypedDict):
    messages: Annotated[list, add_messages]
    next_step: str
    target_language: str


# ==========================================
# Agent Node
# ==========================================

def agent_node(state: GraphState):

    user_message = state["messages"][-1].content

    msg_lower = user_message.lower()

    # Supported languages
    languages = [
        "hindi",
        "french",
        "german",
        "spanish",
        "japanese",
        "english",
        "marathi",
    ]

    detected_language = ""

    for lang in languages:
        if lang in msg_lower:
            detected_language = lang
            break

    if "translate" in msg_lower and detected_language:

        return {
            "next_step": "translate",
            "target_language": detected_language,
            "messages": [
                AIMessage(
                    content=f"Translating to {detected_language.title()}..."
                )
            ]
        }

    return {
        "next_step": "end",
        "target_language": "",
        "messages": [
            AIMessage(
                content="Please use format:\nTranslate <text> to Hindi/French/Spanish/etc."
            )
        ]
    }


# ==========================================
# Translation Node
# ==========================================

def translator_node(state: GraphState):

    user_message = state["messages"][0].content

    target_language = state["target_language"]

    prompt = f"""
    Translate the following text into {target_language}.

    Text:
    {user_message}

    Return ONLY the translated text.
    """

    response = llm.invoke(prompt)

    return {
        "messages": [
            AIMessage(
                content=f"Translation:\n{response.content}"
            )
        ]
    }


# ==========================================
# Router Function
# ==========================================

def route_function(state: GraphState):

    return state["next_step"]


# ==========================================
# Build Graph
# ==========================================

builder = StateGraph(GraphState)

builder.add_node("agent", agent_node)
builder.add_node("translator", translator_node)

builder.set_entry_point("agent")

builder.add_conditional_edges(
    "agent",
    route_function,
    {
        "translate": "translator",
        "end": END
    }
)

builder.add_edge("translator", END)

graph = builder.compile()


# ==========================================
# Chat Loop
# ==========================================

print("Translator Bot Started")
print("Type 'exit' to quit\n")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ],
            "next_step": "",
            "target_language": ""
        }
    )

    print("\nBot:", result["messages"][-1].content)
    print("-" * 50)