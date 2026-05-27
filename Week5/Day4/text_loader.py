from langchain_community.document_loaders import TextLoader
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load txt file
loader = TextLoader("cricket.txt", encoding="utf-8")
docs = loader.load()

# Extract text
text = docs[0].page_content

# Load Ollama model
llm = ChatOllama(model="llama3")

# Prompt
prompt = PromptTemplate(
    input_variables=["topic"],
    template="""
    Summarize the following text in simple words:

    {topic}
    """
)

# Output parser
parser = StrOutputParser()

# Chain
chain = prompt | llm | parser

# Invoke chain
result = chain.invoke({"topic": text})

# Print output
print(result)