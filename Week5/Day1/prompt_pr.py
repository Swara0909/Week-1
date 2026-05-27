from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(
    model="llama3",
    temperature=0.7
)

parser = StrOutputParser()

print("\n===================================")
print("1. SUMMARIZATION CHAIN")
print("===================================")

article = """
Artificial Intelligence is transforming industries by enabling
machines to learn patterns from data. AI is used in healthcare,
finance, recommendation systems, autonomous vehicles,
and customer support systems.
"""

summary_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert text summarizer."
    ),
    (
        "human",
        """
        Summarize the following text in 5 concise points:

        {text}
        """
    )
])

summary_chain = summary_prompt | llm | parser

summary_result = summary_chain.invoke({
    "text": article
})

print(summary_result)

print("\n===================================")
print("2. TRANSLATION CHAIN")
print("===================================")

translation_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a professional language translator."
    ),
    (
        "human",
        """
        Translate the following sentence into {language}:

        {sentence}
        """
    )
])

translation_chain = translation_prompt | llm | parser

translation_result = translation_chain.invoke({
    "language": "French",
    "sentence": "Machine Learning is very interesting."
})

print(translation_result)

print("\n===================================")
print("3. Q&A CHAIN")
print("===================================")

qa_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful AI teacher."
    ),
    (
        "human",
        """
        Answer the following question clearly and simply:

        Question:
        {question}
        """
    )
])

qa_chain = qa_prompt | llm | parser

qa_result = qa_chain.invoke({
    "question": "What is the difference between CNN and RNN?"
})

print(qa_result)

print("\n===================================")
print("4. SENTIMENT ANALYSIS CHAIN")
print("===================================")

review = """
The product quality is amazing and delivery was fast.
I am very happy with the purchase.
"""

sentiment_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a sentiment analysis expert."
    ),
    (
        "human",
        """
        Analyze the sentiment of this review.

        Review:
        {review}

        Return:
        1. Sentiment
        2. Reason
        """
    )
])

sentiment_chain = sentiment_prompt | llm | parser

sentiment_result = sentiment_chain.invoke({
    "review": review
})

print(sentiment_result)


print("\n===================================")
print("5. CODE GENERATION CHAIN")
print("===================================")

code_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert Python developer."
    ),
    (
        "human",
        """
        Generate Python code for the following task:

        {task}

        Add comments in the code.
        """
    )
])

code_chain = code_prompt | llm | parser

code_result = code_chain.invoke({
    "task": "Create a Python function to check palindrome strings"
})

print(code_result)
