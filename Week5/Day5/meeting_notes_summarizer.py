from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

# Load Local Ollama Model
llm = ChatOllama(
    model="llama3",
    temperature=0.7
)

# Prompt Template
prompt = PromptTemplate(
    template="""
You are a Meeting Notes Summarizer.

Summarize the following meeting notes.

Also provide:
1. Key Discussion Points
2. Action Items
3. Deadlines (if mentioned)

Meeting Notes:
{notes}
""",
    input_variables=['notes']
)

# LCEL Chain
chain = prompt | llm | StrOutputParser()

# User Input
meeting_notes = input("Enter Meeting Notes:\n")

# Invoke Chain
result = chain.invoke({
    "notes": meeting_notes
})

# Print Result
print("\n===== GENERATED SUMMARY =====\n")
print(result)

