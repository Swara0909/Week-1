from langchain_community.document_loaders import CSVLoader

# Load CSV file
loader = CSVLoader(file_path="Admission_predict.csv")

# Load documents
docs = loader.load()

# Total rows loaded
print(len(docs))

# First row content
print(docs[4].page_content)

# Metadata
print(docs[0].metadata)