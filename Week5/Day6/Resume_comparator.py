# Multi Resume Comparator — RAG + Tool Calling

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ----------------------------------------
# TOOL: EXTRACT SKILLS
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
# HELPER: LOAD + EMBED RESUME
# ----------------------------------------

def process_resume(pdf_path: str, embeddings):

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    docs = splitter.split_documents(documents)

    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=pdf_path.replace(".pdf", "").replace(" ", "_")
    )

    return vector_store

# ----------------------------------------
# GET SKILLS + CONTEXT
# ----------------------------------------

def get_skills(vector_store, job_description, llm):

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 4}
    )

    relevant_docs = retriever.invoke(job_description)

    context = "\n\n".join(
        doc.page_content for doc in relevant_docs
    )

    llm_with_tools = llm.bind_tools([extract_skills])

    response = llm_with_tools.invoke(
        f"Extract all technical skills from this resume:\n{context}"
    )

    if response.tool_calls:

        for tc in response.tool_calls:

            if tc["name"] == "extract_skills":

                return extract_skills.invoke(tc["args"]), context

    return extract_skills.invoke({"resume": context}), context

# ----------------------------------------
# MAIN
# ----------------------------------------

print("\n===== MULTI RESUME COMPARATOR =====\n")

# ----------------------------------------
# INPUTS
# ----------------------------------------

num_resumes = int(input("Enter number of resumes: "))

resume_paths = []

for i in range(num_resumes):

    path = input(f"Enter path of Resume {i+1}: ").strip()

    resume_paths.append(path)

job_description = input("\nEnter Job Description:\n").strip()

# ----------------------------------------
# SETUP
# ----------------------------------------

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

llm = ChatOllama(
    model="qwen2.5:1.5b",    temperature=0.3
)

# ----------------------------------------
# PROCESS ALL RESUMES
# ----------------------------------------

candidates = []

print("\n[1/3] Loading and Embedding Resumes...\n")

for path in resume_paths:

    vector_store = process_resume(
        path,
        embeddings
    )

    name = path.replace(".pdf", "")

    print(f"Processed: {name}")

    print(f"\nExtracting skills for {name}...\n")

    skills, context = get_skills(
        vector_store,
        job_description,
        llm
    )

    candidates.append({
        "name": name,
        "skills": skills,
        "context": context
    })

print("\nAll resumes processed successfully.")

# ----------------------------------------
# BUILD COMPARISON TEXT
# ----------------------------------------

candidate_text = ""

for i, candidate in enumerate(candidates, start=1):

    candidate_text += f"""
Candidate {i}: {candidate['name']}

Resume:
{candidate['context']}

Skills:
{candidate['skills']}

"""

# ----------------------------------------
# FINAL COMPARISON PROMPT
# ----------------------------------------

prompt = PromptTemplate(
    template="""
You are a senior recruiter.

Compare all candidates for the following job.

Job Description:
{job_description}

Candidates:
{candidate_text}

Provide:

1. Comparison Table
2. Match Percentage for each candidate
3. Strengths and Weaknesses
4. Rank all candidates from best to worst
5. Final Hiring Recommendation
""",
    input_variables=[
        "job_description",
        "candidate_text"
    ]
)

# ----------------------------------------
# FINAL LLM ANALYSIS
# ----------------------------------------

print("\n[3/3] Comparing Candidates...\n")

llm_plain = ChatOllama(
    model="llama3",
    temperature=0.7
)

chain = prompt | llm_plain | StrOutputParser()

result = chain.invoke({
    "job_description": job_description,
    "candidate_text": candidate_text
})

# ----------------------------------------
# OUTPUT
# ----------------------------------------

print("\n===== FINAL COMPARISON RESULT =====\n")

print(result)