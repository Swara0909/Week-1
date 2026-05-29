# pdf_qa_agent.py

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama

from langchain.chains import RetrievalQA

# ----------------------------------------
# LOAD PDF
# ----------------------------------------

pdf_path = "Swara Resume.pdf"

loader = PyPDFLoader(pdf_path)

documents = loader.load()

print("PDF Loaded Successfully")

# ----------------------------------------
# SPLIT DOCUMENTS
# ----------------------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100
)

docs = text_splitter.split_documents(documents)

print("Documents Split Successfully")

# ----------------------------------------
# CREATE EMBEDDINGS
# ----------------------------------------

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# ----------------------------------------
# CREATE VECTOR DATABASE
# ----------------------------------------

vectorstore = FAISS.from_documents(
    docs,
    embeddings
)

print("Vector DB Created")

# ----------------------------------------
# CREATE RETRIEVER
# ----------------------------------------

retriever = vectorstore.as_retriever()

# ----------------------------------------
# LOAD LLM
# ----------------------------------------

llm = ChatOllama(
    model="llama3",
    temperature=0
)

# ----------------------------------------
# CREATE RAG QA CHAIN
# ----------------------------------------

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever
)

# ----------------------------------------
# QUESTION LOOP
# ----------------------------------------

while True:

    question = input("\nAsk Question (type exit to quit): ")

    if question.lower() == "exit":
        break

    result = qa_chain.invoke({
        "query": question
    })

    print("\n===== ANSWER =====\n")

    print(result["result"])