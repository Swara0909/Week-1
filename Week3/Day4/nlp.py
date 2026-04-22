import nltk

nltk.download('punkt')
nltk.download('punkt_tab') 

from nltk.tokenize import word_tokenize, sent_tokenize

text = "I love machine learning. NLP is amazing!"

# Word Tokenization
words = word_tokenize(text)
print(words)

# Sentence Tokenization
sentences = sent_tokenize(text)
print(sentences)