from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import json
import os

topic = input("\nEnter a technical topic: ")

llm = ChatOllama(
    model="llama3",
    temperature=0.7
)

parser = StrOutputParser()

technical_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a senior AI engineer and technical educator.
        Explain technical concepts clearly for beginners.
        """
    ),

    (
        "human",
        """
        Explain {topic} in beginner-friendly language.

        Include:
        1. Definition
        2. How it works
        3. Advantages
        4. Applications
        5. Challenges

        Use simple language.
        """
    )
])

architecture_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an expert software architect.
        """
    ),
    (
        "human",
        """
        Generate a system architecture summary for {topic}.

        Include:
        - Main Components
        - Workflow
        - Technologies Used
        - Data Flow

        Return in structured bullet points.
        """
    )
])


technical_chain = technical_prompt | llm | parser

architecture_chain = architecture_prompt | llm | parser


technical_result = technical_chain.invoke({
    "topic": topic
})

architecture_result = architecture_chain.invoke({
    "topic": topic
})

## Structured output
documentation = {
    "topic": topic,
    "technical_explanation": technical_result,
    "architecture_summary": architecture_result
}


# Output folder
os.makedirs("output", exist_ok=True)

#Export json file
with open("output/documentation.json", "w", encoding="utf-8") as file:
    json.dump(documentation, file, indent=4)


print("\n========================================")
print("TECHNICAL EXPLANATION")
print("========================================\n")

print(technical_result)

print("\n========================================")
print("ARCHITECTURE SUMMARY")
print("========================================\n")

print(architecture_result)

print("\n========================================")
print("OUTPUT EXPORTED SUCCESSFULLY")
print("File: output/documentation.json")
print("========================================")