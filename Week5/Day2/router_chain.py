from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

# =====================================================
# LOCAL OLLAMA MODEL
# =====================================================

llm = ChatOllama(
    model="llama3",
    temperature=0.7
)

# =====================================================
# OUTPUT PARSER
# =====================================================

parser = StrOutputParser()

# =====================================================
# 1. SUMMARIZATION CHAIN
# =====================================================

summary_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert text summarizer."
    ),
    (
        "human",
        """
        Summarize the following text in 5 concise points:

        {input}
        """
    )
])

summary_chain = summary_prompt | llm | parser

# =====================================================
# 2. TRANSLATION CHAIN
# =====================================================

translation_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a professional language translator."
    ),
    (
        "human",
        """
        Translate the following sentence into French:

        {input}
        """
    )
])

translation_chain = translation_prompt | llm | parser

# =====================================================
# 3. Q&A CHAIN
# =====================================================

qa_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful AI teacher."
    ),
    (
        "human",
        """
        Answer the following question clearly and simply:

        {input}
        """
    )
])

qa_chain = qa_prompt | llm | parser

# =====================================================
# 4. SENTIMENT ANALYSIS CHAIN
# =====================================================

sentiment_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a sentiment analysis expert."
    ),
    (
        "human",
        """
        Analyze the sentiment of this review:

        {input}

        Return:
        - Sentiment
        - Reason
        """
    )
])

sentiment_chain = sentiment_prompt | llm | parser

# =====================================================
# 5. CODE GENERATION CHAIN
# =====================================================

code_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert Python developer."
    ),
    (
        "human",
        """
        Generate Python code for the following task:

        {input}

        Add comments in code.
        """
    )
])

code_chain = code_prompt | llm | parser

# =====================================================
# ROUTER FUNCTION
# =====================================================

def router(info):

    task = info["task"]

    if task == "summarize":
        return summary_chain

    elif task == "translate":
        return translation_chain

    elif task == "qa":
        return qa_chain

    elif task == "sentiment":
        return sentiment_chain

    elif task == "code":
        return code_chain

    else:
        raise ValueError("Invalid task selected")

# =====================================================
# ROUTER CHAIN
# =====================================================

router_chain = RunnableLambda(router)

# =====================================================
# USER INPUT
# =====================================================

print("\n===================================")
print("ROUTER CHAIN AI ASSISTANT")
print("===================================")

print("""
Choose Task:
1. summarize
2. translate
3. qa
4. sentiment
5. code
""")

task = input("Enter task: ")

user_input = input("\nEnter your input:\n")

# =====================================================
# FINAL CHAIN
# =====================================================

final_chain = router_chain

selected_chain = final_chain.invoke({
    "task": task
})

# =====================================================
# RUN SELECTED CHAIN
# =====================================================

result = selected_chain.invoke({
    "input": user_input
})

# =====================================================
# PRINT RESULT
# =====================================================

print("\n===================================")
print("RESULT")
print("===================================\n")

print(result)