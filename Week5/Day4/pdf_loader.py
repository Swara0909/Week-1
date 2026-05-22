from langchain_community.document_loaders import PyPDFLoader

# Load PDF
loader = PyPDFLoader("Langchain 5 Day Intensive Bootcamp Program.pdf")

# Load documents
docs = loader.load()

# Print type
print(type(docs))

# Number of pages/documents
print(len(docs))

# First page content
print(docs[0].page_content)

# Metadata
print(docs[0].metadata)

# go to python langchain docs/document loaders too get various doc loaders as per use case