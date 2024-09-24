# Continuous Bag of Words (CBOW)

## Overview
The **Continuous Bag of Words (CBOW)** model is a neural network architecture used for learning word embeddings in Natural Language Processing (NLP). It predicts a target word based on its surrounding context words. The CBOW model is a foundational component of the Word2Vec framework.

## Key Concepts

### 1. **Input and Output**
- **Input**: The model takes a set of context words surrounding a target word.
- **Output**: The model predicts the target word.

### 2. **Architecture**
- The CBOW model consists of:
  - An input layer where context words are represented as one-hot encoded vectors.
  - A hidden layer that computes the average of the input vectors.
  - An output layer that predicts the target word.

### 3. **Training Objective**
- The objective is to maximize the probability of predicting the correct target word given the context words.

### 4. **Example**
- For the sentence "The cat sits on the mat", if the context window size is 2:
  - Context: ["The", "cat", "on", "the"]
  - Target: "sits"

### 5. **Applications**
- CBOW is used in various NLP tasks, including word embeddings, sentiment analysis, and document classification.

## Conclusion
The CBOW model effectively captures semantic relationships between words by leveraging context, making it a powerful tool in the field of Natural Language Processing.
