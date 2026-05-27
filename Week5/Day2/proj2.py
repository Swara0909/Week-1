import asyncio
from pydantic import BaseModel, Field
from typing import List, Literal
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

# ==========================================
# PHASE 1: DATA ARCHITECTURE (SCHEMAS)
# ==========================================

class Task(BaseModel):
    title: str = Field(description="A short, actionable title for the developer task")
    description: str = Field(description="Technical details on how to implement this task")

class UserStory(BaseModel):
    title: str = Field(description="Short title of the feature")
    description: str = Field(description="The 'As a... I want... so that...' story format")
    priority: Literal["Low", "Medium", "High", "Critical"] = Field(description="Business priority")
    acceptance_criteria: List[str] = Field(description="List of conditions that must be met")
    estimated_hours: int = Field(description="Estimated development hours (between 1 and 40)")
    tasks: List[Task] = Field(description="A list of technical developer tasks required to build this story")

class RequirementAnalysis(BaseModel):
    stories: List[UserStory] = Field(description="The list of user stories extracted from the raw text")

# ==========================================
# PHASE 2: ASYNC EXTRACTION PIPELINE
# ==========================================

async def extract_requirements(raw_text: str) -> RequirementAnalysis:
    """Takes messy meeting notes and extracts structured JSON requirements."""
    
    # We use a temperature of 0 because we want strict, factual extraction, not creativity
    llm = ChatOllama(model="llama3.2:latest", temperature=0)
    
    # Apply our Retry Logic!
    structured_llm = llm.with_structured_output(RequirementAnalysis).with_retry(stop_after_attempt=3)
    
    # A strict system prompt to guide the small model
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert Agile Product Owner. 
        Extract user stories and technical developer tasks from the following meeting notes. 
        You MUST strictly follow the requested JSON schema. Do not include placeholders."""),
        ("human", "{text}")
    ])
    
    chain = prompt | structured_llm
    
    # Notice the ainvoke for async execution
    return await chain.ainvoke({"text": raw_text})

# ==========================================
# PHASE 3: INTERACTIVE AGENT WITH MEMORY
# ==========================================

async def main():
    print("Welcome to the AI Requirements Analyzer")
    print("-" * 50)
    
    # 1. Get the raw input
    print("\nPaste your raw meeting notes below (Press Enter twice when done):")
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)
    raw_notes = "\n".join(lines)
    
    if len(raw_notes.strip()) < 10:
        print("Input Guardrail Triggered: Notes are too short!")
        return

    # 2. Run the async extraction
    print("\nExtracting structured requirements... (This might take a moment)")
    try:
        analysis = await extract_requirements(raw_notes)
    except Exception as e:
        print(f"\nPipeline failed even after retries: {e}")
        return

    # 3. Display the structured output
    print("\nExtraction Complete!")
    print("=" * 50)
    for i, story in enumerate(analysis.stories):
        print(f"\nStory {i+1}: {story.title} [Priority: {story.priority} | {story.estimated_hours} hrs]")
        print(f"   {story.description}")
        print("   Tasks:")
        for task in story.tasks:
            print(f"    - {task.title}")
            
    # 4. Initialize the Chat Agent with Memory
    print("\n" + "=" * 50)
    print("🗣️  Chat Session Started. Ask me about these requirements! (Type 'quit' to exit)")
    
    chat_llm = ChatOllama(model="llama3.2:latest")
    chat_history = [
        SystemMessage(content="You are a helpful product requirements assistant."),
        SystemMessage(
            content="Here is the structured requirement data I just extracted from the meeting: "
            + analysis.model_dump_json()
        ),
    ]

    # 5. The Chat Loop
    while True:
        user_msg = input("\nYou: ")
        if user_msg.lower() in ['quit', 'exit']:
            print("Goodbye!")
            break

        chat_history.append(HumanMessage(content=user_msg))
        response = chat_llm.invoke(chat_history)
        print("\nAI:", response.content)
        chat_history.append(AIMessage(content=response.content))

# Run the async main loop
if __name__ == "__main__":
    asyncio.run(main())