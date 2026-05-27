from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
import json

# Initialize model
llm = ChatOllama(
    model="qwen2.5:1.5b",
    temperature=0.7
)

# User input
topic = input("Enter a topic: ")

# -------------------------------
# Technical Explanation Prompt
# -------------------------------

technical_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a technical expert with deep knowledge of {topic}."
    ),
    (
        "human",
        "Provide a beginner-friendly technical explanation of {topic}."
    )
])

technical_chain = technical_prompt | llm

technical_response = technical_chain.invoke({
    "topic": topic
})

# -------------------------------
# Architecture Summary Prompt
# -------------------------------

architecture_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a software architect specializing in AI systems."
    ),
    (
        "human",
        "Generate a simple architecture workflow summary for {topic}."
    )
])

architecture_chain = architecture_prompt | llm

architecture_response = architecture_chain.invoke({
    "topic": topic
})

# -------------------------------
# Structured Output
# -------------------------------

output = {
    "topic": topic,
    "technical_explanation": technical_response.content,
    "architecture_summary": architecture_response.content
}

# Export to JSON
with open("output.json", "w") as f:
    json.dump(output, f, indent=4)

# Print Results
print("\n=== Technical Explanation ===\n")
print(technical_response.content)

print("\n=== Architecture Summary ===\n")
print(architecture_response.content)

print("\nOutput exported to output.json")