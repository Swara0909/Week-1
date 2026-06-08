import sys
import os
from typing import TypedDict

from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END

from langchain_huggingface import (
    HuggingFaceEndpoint,
    ChatHuggingFace
)


load_dotenv("../.env")

hf_token = os.getenv("HF_TOKEN")


# LangChain Hugging Face LLM

base_llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    huggingfacehub_api_token=hf_token,
    max_new_tokens=300,
    temperature=0.7
)

llm = ChatHuggingFace(llm=base_llm)

# --------------------------------------------------
# State
# --------------------------------------------------

class ResearchState(TypedDict):
    topic: str
    benefits: str
    risks: str
    alternatives: str
    final_summary: str

# --------------------------------------------------
# Branch 1 : Benefits
# --------------------------------------------------

def research_benefits(state: ResearchState):

    topic = state["topic"]

    print(f"[Branch 1] Researching Benefits of '{topic}'...")

    response = llm.invoke(
        f"""
        Give 4 important benefits of {topic}.

        Return only bullet points.
        """
    )

    return {
        "benefits": response.content
    }

# --------------------------------------------------
# Branch 2 : Risks
# --------------------------------------------------

def research_risks(state: ResearchState):

    topic = state["topic"]

    print(f"[Branch 2] Researching Risks of '{topic}'...")

    response = llm.invoke(
        f"""
        Give 4 important risks of {topic}.

        Return only bullet points.
        """
    )

    return {
        "risks": response.content
    }

# --------------------------------------------------
# Branch 3 : Alternatives
# --------------------------------------------------

def research_alternatives(state: ResearchState):

    topic = state["topic"]

    print(f"[Branch 3] Researching Alternatives of '{topic}'...")

    response = llm.invoke(
        f"""
        Give 4 alternatives to {topic}.

        Return only bullet points.
        """
    )

    return {
        "alternatives": response.content
    }

# --------------------------------------------------
# Fan-In / Reduce Node
# --------------------------------------------------

def combine_summary(state: ResearchState):

    topic = state["topic"]

    print(f"[Combine] Generating Final Summary...")

    response = llm.invoke(
        f"""
        Topic: {topic}

        Benefits:
        {state['benefits']}

        Risks:
        {state['risks']}

        Alternatives:
        {state['alternatives']}

        Create a concise research summary
        in 2-3 paragraphs.
        """
    )

    return {
        "final_summary": response.content
    }


def build_graph():

    builder = StateGraph(ResearchState)

    builder.add_node("benefits", research_benefits)
    builder.add_node("risks", research_risks)
    builder.add_node("alternatives", research_alternatives)
    builder.add_node("combine", combine_summary)

    # Fan-Out
    builder.add_edge(START, "benefits")
    builder.add_edge(START, "risks")
    builder.add_edge(START, "alternatives")

    # Fan-In
    builder.add_edge("benefits", "combine")
    builder.add_edge("risks", "combine")
    builder.add_edge("alternatives", "combine")

    builder.add_edge("combine", END)

    return builder.compile()


def run(topic: str):

    graph = build_graph()

    result = graph.invoke(
        {
            "topic": topic,
            "benefits": "",
            "risks": "",
            "alternatives": "",
            "final_summary": ""
        }
    )

    return result


if __name__ == "__main__":

    topic = input("Enter Research Topic: ")

    print("\n" + "=" * 60)
    print("Research Summarizer")
    print("Topic:", topic)
    print("=" * 60)

    result = run(topic)

    print("\nBENEFITS")
    print(result["benefits"])

    print("\nRISKS")
    print(result["risks"])

    print("\nALTERNATIVES")
    print(result["alternatives"])

    print("\nFINAL SUMMARY")
    print(result["final_summary"])

    print("\n" + "=" * 60)