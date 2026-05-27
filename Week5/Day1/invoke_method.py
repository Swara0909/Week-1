from langchain_ollama import ChatOllama

# Initialize local model
llm = ChatOllama(
    model="llama3",
    temperature=0.7
)

# Ask question
response = llm.invoke(
    "Explain Rainbow in 3 sentences"
)

# Print response
print("\nAI Response:\n")
print(response.content)


