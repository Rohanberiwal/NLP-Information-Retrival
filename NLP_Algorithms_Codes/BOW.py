from sklearn.feature_extraction.text import CountVectorizer

# Sample data
corpus = [
    "The cat sat on the mat.",
    "The dog sat on the mat."
]

# Create the BoW model
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)

# Convert to an array
print(X.toarray())

# Print the vocabulary
print(vectorizer.get_feature_names_out())
