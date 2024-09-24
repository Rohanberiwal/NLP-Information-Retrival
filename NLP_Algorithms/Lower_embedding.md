# Low-Dimensional Embedding in NLP

## Definition
Low-dimensional embeddings represent words or phrases as vectors in a reduced vector space, typically with dimensions ranging from 50 to 300.

## Original Input Space
- Traditional representations (e.g., one-hot encoding) create high-dimensional vectors where each word is unique.
  - **Example**: 
    - **Vocabulary Size**: 100,000 words → One-hot vector of length 100,000.

## Transformation
- **From High-Dimensional to Low-Dimensional**: Instead of using large, sparse vectors, words are mapped to dense vectors in a smaller dimension.

## Benefits
- **Efficiency**: Reduced storage and faster computation.
- **Semantic Relationships**: Similar words are closer in the embedding space, allowing models to better capture meanings and relationships.

## Example
- In a low-dimensional space of 100 dimensions, "king" and "queen" might have vectors that are close to each other, reflecting their similar meanings.

## Conclusion
Low-dimensional embeddings are fundamental to various NLP tasks, enhancing the ability to process and understand language.
