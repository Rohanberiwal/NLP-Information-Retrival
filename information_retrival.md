# Information Retrieval Techniques

## 1. Document Indexing
- Indexing involves organizing documents for efficient searching.
- **Inverted Index**: Maps each word to the documents containing it.
- **Forward Index**: Stores terms present in a document but is slower for search.

**Example**: 
If the document is "cat sat on mat", the inverted index would map:


## 2. Query Processing
- Processes user queries to retrieve relevant documents.
- **Types of Queries**:
  - **Boolean Queries**: Use logical operators (AND, OR, NOT).
  - **Phrase Queries**: Search for exact phrases.
  - **Fuzzy Queries**: Allow approximate matching.

## 3. Ranking Algorithms
- **Ranking** prioritizes documents relevant to the user query.
- **TF-IDF (Term Frequency-Inverse Document Frequency)**: Calculates the importance of words.
  - **TF (Term Frequency)**: How frequently a word appears in a document.
  - **IDF (Inverse Document Frequency)**: How rare a word is across all documents.
- **Cosine Similarity**: Measures similarity between vectors (query and document).

**Example**: 
If "dog" appears frequently in a document, TF-IDF gives it a higher score.

## 4. Tokenization and Preprocessing
- **Tokenization**: Splitting text into meaningful words (tokens).
- **Stopword Removal**: Removing common unimportant words (e.g., "the", "is").
- **Stemming and Lemmatization**: Reducing words to their base form.

## 5. Vector Space Model (VSM)
- Represents documents and queries as vectors in a multi-dimensional space.
- **Similarity between Vectors**: Documents are ranked based on the similarity to the query vector.

**Example**: 
Query vector `q = [1, 0, 1]` and document vector `d = [1, 1, 0]` use cosine similarity for comparison.

## 6. TF-IDF (Term Frequency-Inverse Document Frequency)
- Evaluates the importance of a word in a document relative to the dataset.
  
**Formula**:
