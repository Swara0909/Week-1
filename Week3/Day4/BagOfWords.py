from sklearn.feature_extraction.text import CountVectorizer

documents=[
    "I love machine learning",
    "I love AI",
    "ML is fun"
]

vectorizer=CountVectorizer()

X=vectorizer.fit_transform(documents)

print(vectorizer.get_feature_names_out())
print(X.toarray())