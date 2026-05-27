from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

# Local Ollama model
llm = ChatOllama(
    model="llama3",
    temperature=0.7
)

# Prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI architect"),
    ("human", "Explain {topic}")
])

# LCEL chain
chain = prompt | llm | StrOutputParser()

# Run chain
result = chain.invoke({
    "topic": "RAG"
})

print(result)