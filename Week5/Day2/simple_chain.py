from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

# Local Ollama model
llm = ChatOllama(
    model="llama3",
    temperature=0.7
)

# Prompt template
prompt = PromptTemplate(
    template=" generate 5 interesting facts about {topic}",
    input_variables=['topic']
)

# LCEL chain
chain = prompt | llm | StrOutputParser()

# Run chain
result = chain.invoke({
    "topic": "RAG"
})

print(result)

# chain.get_graph().print_ascii()