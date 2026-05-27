from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

# Local Ollama model
llm1 = ChatOllama(
    model="llama3",
    temperature=0.7
)

llm2 = ChatOllama(
    model="qwen2.5",
    temperature=0.7
)

# Prompt template
prompt1 = PromptTemplate(
    template=" generate short and simple notes from the following text \n {text}",
    input_variables=['text']
)

prompt2 = PromptTemplate(
    template=" generate 5 short ques from the following text \n {text}",
    input_variables=['text']
)

prompt3=PromptTemplate(
    template='Merge the provided notes and quiz into a single document \n notes -> {notes} and quiz -> {quiz}',
    input_variables=['notes', 'quiz']
)

parser=StrOutputParser()

parallel_chain =  RunnableParallel({
    'notes': prompt1 | llm1 | parser,
    'quiz': prompt2 | llm2 | parser
})

# Run chain
merge_chain = prompt3|llm1|parser

chain=parallel_chain|merge_chain

text='''
Support Vector Machine (SVM) is a supervised machine learning algorithm used for classification and regression tasks. 
It identifies the optimal boundary, known as a hyperplane, to separate different classes in a dataset. 
SVM focuses on maximizing the margin between classes, which improves prediction accuracy and generalization. It works effectively for both linear and non-linear data using kernel functions. 
SVM is widely applied in spam detection, image classification, handwriting recognition, medical diagnosis, and text analysis because of its high accuracy and robustness.

'''
result=chain.invoke({'text':text})
print(result)

