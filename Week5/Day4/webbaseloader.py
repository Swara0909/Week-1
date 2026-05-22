from langchain_community.document_loaders import WebBaseLoader
from langchain_community.chat_models import ChatOllama

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load website
loader = WebBaseLoader("https://python.langchain.com")

docs = loader.load()

# Extract website text
text = docs[0].page_content

# Load Ollama model
llm = ChatOllama(model="llama3")

# Prompt Template
prompt = PromptTemplate(
    input_variables=["content"],
    template="""
    Summarize the following website content in simple words:

    {content}
    """
)

# Output Parser
parser = StrOutputParser()

# Chain
chain = prompt | llm | parser

# Run chain
result = chain.invoke({"content": text})

# Print output
print(result)

# # Print content
# print(docs[0].page_content)

# # Print metadata
# print(docs[0].metadata)