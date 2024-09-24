from sklearn.feature_extraction.text import CountVectorizer

# Sample data
corpus = [
    "The cat sat on the mat.",
    "The dog sat on the mat."
]

# Create the Bag of N-Grams model (n=2 for bigrams)
vectorizer = CountVectorizer(ngram_range=(2, 2))
X = vectorizer.fit_transform(corpus)

# Convert to an array
print(X.toarray())

# Print the bigram vocabulary
print(vectorizer.get_feature_names_out())
