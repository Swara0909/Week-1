# Resume Screening Assistant — Basic RAG + Tool Calling

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ----------------------------------------
# STEP 1 — LOAD PDF
# ----------------------------------------

loader = PyPDFLoader("Swara Resume.pdf")
documents = loader.load()
print("PDF Loaded")

# ----------------------------------------
# STEP 2 — SPLIT INTO CHUNKS
# ----------------------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

docs = text_splitter.split_documents(documents)
print(f"Split into {len(docs)} chunks")

# ----------------------------------------
# STEP 3 — STORE IN VECTOR DB (RAG)
# ----------------------------------------

embeddings = OllamaEmbeddings(model="nomic-embed-text")

vector_store = Chroma.from_documents(
    documents=docs,
    embedding=embeddings
)

print("Vector Store Created")

# ----------------------------------------
# STEP 4 — TOOL: EXTRACT SKILLS
# ----------------------------------------

@tool
def extract_skills(resume: str) -> str:
    """Extract technical skills from resume text."""

    skills = [
        "Python", "Java", "C", "C++", "SQL",
        "Machine Learning", "Deep Learning",
        "Flask", "Django", "React", "Node.js",
        "HTML", "CSS", "JavaScript",
        "LangChain", "AI", "MongoDB"
    ]

    found = [s for s in skills if s.lower() in resume.lower()]
    return f"Extracted Skills: {', '.join(found)}"

# ----------------------------------------
# STEP 5 — JOB DESCRIPTION INPUT
# ----------------------------------------

job_description = input("\nEnter Job Description:\n")

# ----------------------------------------
# STEP 6 — RAG: RETRIEVE RELEVANT CHUNKS
# ----------------------------------------

# Instead of sending the full resume, retrieve only the most relevant parts
retriever = vector_store.as_retriever(search_kwargs={"k": 4})
relevant_docs = retriever.invoke(job_description)

# Build context from retrieved chunks
retrieved_context = "\n\n".join(doc.page_content for doc in relevant_docs)

print(f"\nRetrieved {len(relevant_docs)} relevant chunks from resume")

# ----------------------------------------
# STEP 7 — EXTRACT SKILLS USING TOOL
# ----------------------------------------

llm = ChatOllama(model="qwen2.5", temperature=0.3)
llm_with_tools = llm.bind_tools([extract_skills])

tool_response = llm_with_tools.invoke(
    f"Extract all technical skills from this resume text:\n{retrieved_context}"
)

extracted_skills = "N/A"

if tool_response.tool_calls:
    for tc in tool_response.tool_calls:
        if tc["name"] == "extract_skills":
            extracted_skills = extract_skills.invoke(tc["args"])
else:
    # Fallback: run tool directly
    extracted_skills = extract_skills.invoke({"resume": retrieved_context})

print(f"\n{extracted_skills}")

# ----------------------------------------
# STEP 8 — SCREEN AGAINST JD
# ----------------------------------------

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

Resume (most relevant sections):
{resume}

Extracted Skills:
{skills}

Job Description:
{job_description}
""",
    input_variables=["resume", "skills", "job_description"]
)

llm_plain = ChatOllama(model="llama3", temperature=0.7)
chain = prompt | llm_plain | StrOutputParser()

result = chain.invoke({
    "resume": retrieved_context,
    "skills": extracted_skills,
    "job_description": job_description
})

print("\n===== RESUME ANALYSIS =====\n")
print(result)