# Resume Screening Assistant using Ollama + LangChain

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

# -----------------------------
# LOAD PDF RESUME
# -----------------------------

# Give your resume PDF path here
loader = PyPDFLoader("Swara Resume.pdf")

documents = loader.load()

print("PDF Loaded")

# -----------------------------
# SPLIT TEXT
# -----------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100
)

docs = text_splitter.split_documents(documents)

# Combine chunks into one text
resume_text = ""

for doc in docs:
    resume_text += doc.page_content + "\n"

# -----------------------------
# JOB DESCRIPTION INPUT
# -----------------------------

job_description = input("Enter Job Description:\n")

# -----------------------------
# LOAD OLLAMA MODEL
# -----------------------------

llm = ChatOllama(
    model="llama3",
    temperature=0.7
)

# -----------------------------
# PROMPT TEMPLATE
# -----------------------------

prompt = PromptTemplate(
    template="""
You are an AI Resume Screening Assistant.

Analyze the resume against the job description.

Provide:
1. Candidate Summary
2. Matching Skills
3. Missing Skills
4. Match Percentage
5. Final Recommendation

Resume:
{resume}

Job Description:
{job_description}
""",
    input_variables=["resume", "job_description"]
)

chain = prompt | llm | StrOutputParser()

result = chain.invoke({
    "resume": resume_text,
    "job_description": job_description
})

print("\n===== RESUME ANALYSIS =====\n")
print(result)
