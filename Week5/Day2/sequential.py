from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

# Local Ollama model
llm = ChatOllama(
    model="llama3",
    temperature=0.7
)

# Prompt template
prompt1 = PromptTemplate(
    template=" generate a detailed report on {topic}",
)

prompt2 = PromptTemplate(
    template=" generate 5 pointer summary from the following text \n {text}",
    input_variables=['text']
)

parser=StrOutputParser
# LCEL chain
chain = prompt1 | llm | prompt2 | llm | parser

# Run chain
result = chain.invoke({
    "topic": "Unemployment in India"
})

print(result)

