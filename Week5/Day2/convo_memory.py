from langchain_ollama import ChatOllama
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# =====================================================
# MODEL
# =====================================================

llm = ChatOllama(
    model="phi3",
    temperature=0.7
)

# =====================================================
# MEMORY
# =====================================================

memory = ConversationBufferMemory()

# =====================================================
# OUTPUT PARSER
# =====================================================

parser = StrOutputParser()

# =====================================================
# CHAT PROMPT
# =====================================================

prompt = ChatPromptTemplate.from_messages([

    (
        "system",
        """
        You are a helpful AI assistant.
        Use previous conversation context while replying.
        """
    ),

    (
        "human",
        """
        Conversation History:
        {history}

        User Question:
        {question}
        """
    )
])

# =====================================================
# CHAT LOOP
# =====================================================

print("\n===================================")
print("AI CHATBOT WITH MEMORY")
print("Type 'exit' to stop")
print("===================================\n")

while True:

    question = input("You: ")

    if question.lower() == "exit":
        break

    # Load previous memory
    history = memory.load_memory_variables({})["history"]

    # Create chain
    chain = prompt | llm | parser

    # Generate response
    response = chain.invoke({
        "history": history,
        "question": question
    })

    # Print AI response
    print("\nAI:", response)

    # Save conversation
    memory.save_context(
        {"input": question},
        {"output": response}
    )