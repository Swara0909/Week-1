from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import (
    StrOutputParser,
    PydanticOutputParser
)
from langchain_core.runnables import (
    RunnableBranch,
    RunnableLambda
)

from pydantic import BaseModel, Field
from typing import Literal

# =====================================================
# LOCAL OLLAMA MODEL
# =====================================================

model = ChatOllama(
    model="phi3",   # lightweight model
    temperature=0.7
)

# =====================================================
# STRING OUTPUT PARSER
# =====================================================

parser = StrOutputParser()

# =====================================================
# PYDANTIC MODEL
# =====================================================

class Feedback(BaseModel):

    feedback: str = Field(
        description="Original feedback text"
    )

    sentiment: Literal['positive', 'negative'] = Field(
        description='Sentiment of the feedback'
    )

# =====================================================
# PYDANTIC PARSER
# =====================================================

parser2 = PydanticOutputParser(
    pydantic_object=Feedback
)

# =====================================================
# CLASSIFICATION PROMPT
# =====================================================

prompt1 = PromptTemplate(
    template="""
    Analyze the sentiment of the following feedback.

    Feedback:
    {feedback}

    Return:
    - feedback
    - sentiment

    {format_instruction}
    """,

    input_variables=['feedback'],

    partial_variables={
        'format_instruction':
        parser2.get_format_instructions()
    }
)

# =====================================================
# SENTIMENT CLASSIFIER CHAIN
# =====================================================

classifier_chain = prompt1 | model | parser2

# =====================================================
# POSITIVE RESPONSE PROMPT
# =====================================================

prompt2 = PromptTemplate(
    template="""
    Write a polite and professional response
    to this positive feedback:

    {feedback}
    """,

    input_variables=['feedback']
)

# =====================================================
# NEGATIVE RESPONSE PROMPT
# =====================================================

prompt3 = PromptTemplate(
    template="""
    Write a polite apology and support response
    to this negative feedback:

    {feedback}
    """,

    input_variables=['feedback']
)

# =====================================================
# POSITIVE RESPONSE CHAIN
# =====================================================

positive_chain = (
    RunnableLambda(lambda x: {
        "feedback": x.feedback
    })
    | prompt2
    | model
    | parser
)

# =====================================================
# NEGATIVE RESPONSE CHAIN
# =====================================================

negative_chain = (
    RunnableLambda(lambda x: {
        "feedback": x.feedback
    })
    | prompt3
    | model
    | parser
)

# =====================================================
# ROUTER / BRANCH CHAIN
# =====================================================

branch_chain = RunnableBranch(

    (
        lambda x: x.sentiment == 'positive',
        positive_chain
    ),

    (
        lambda x: x.sentiment == 'negative',
        negative_chain
    ),

    RunnableLambda(
        lambda x: "Could not determine sentiment"
    )
)

# =====================================================
# FINAL CHAIN
# =====================================================

chain = classifier_chain | branch_chain

# =====================================================
# USER INPUT
# =====================================================

feedback = input("\nEnter customer feedback:\n")

# =====================================================
# RUN CHAIN
# =====================================================

result = chain.invoke({
    'feedback': feedback
})

# =====================================================
# PRINT RESULT
# =====================================================

print("\n===================================")
print("AI RESPONSE")
print("===================================\n")

print(result)