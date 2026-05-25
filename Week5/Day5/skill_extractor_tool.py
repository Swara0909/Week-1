# resume_skill_extractor.py

from langchain_core.tools import tool
from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import ChatOllama

# -----------------------------
# LOAD PDF USING DOCUMENT LOADER
# -----------------------------

pdf_path = "Swara Resume.pdf"

loader = PyPDFLoader(pdf_path)

documents = loader.load()

# Combine all pages into one text
resume_text = ""

for doc in documents:
    resume_text += doc.page_content + "\n"

# -----------------------------
# TOOL CREATION
# -----------------------------

@tool
def extract_skills(resume: str) -> str:
    """
    Extract technical skills from resume text.
    """

    skills = [
        "Python", "Java", "C", "C++", "SQL",
        "Machine Learning", "Deep Learning",
        "Flask", "Django", "React", "Node.js",
        "HTML", "CSS", "JavaScript",
        "LangChain", "AI", "MongoDB"
    ]

    found_skills = []

    for skill in skills:

        if skill.lower() in resume.lower():
            found_skills.append(skill)

    return f"Extracted Skills: {', '.join(found_skills)}"

# -----------------------------
# LOAD OLLAMA MODEL
# -----------------------------

llm = ChatOllama(
    model="qwen2.5",
    temperature=0.7
)

# -----------------------------
# BIND TOOL
# -----------------------------

llm_with_tools = llm.bind_tools([extract_skills])

# -----------------------------
# USER QUERY
# -----------------------------

query = f"""
Analyze this resume and extract all technical skills.

Resume:
{resume_text}
"""

# -----------------------------
# INVOKE MODEL
# -----------------------------

response = llm_with_tools.invoke(query)

# -----------------------------
# TOOL EXECUTION
# -----------------------------

if response.tool_calls:

    for tool_call in response.tool_calls:

        # print(tool_call) for metadata

        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        if tool_name == "extract_skills":

            result = extract_skills.invoke(tool_args)

            print("\n===== EXTRACTED SKILLS =====\n")
            print(result)

else:
    print("No tool was called.")