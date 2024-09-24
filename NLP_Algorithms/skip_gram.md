# Skip-Gram Model

## Overview
The **Skip-Gram** model is a neural network architecture used for learning word embeddings in Natural Language Processing (NLP). It predicts the context words surrounding a target word, effectively capturing the relationships and semantics between words.

## Key Concepts

### 1. **Input and Output**
- **Input**: The model takes a target word as input, represented as a one-hot encoded vector.
- **Output**: It predicts multiple context words based on the target word within a defined window size.

### 2. **Architecture**
- The Skip-Gram model consists of:
  - **Input Layer**: Where the target word is represented as a one-hot vector.
  - **Hidden Layer**: A weight matrix that connects the input layer to the output layer.
  - **Output Layer**: A softmax layer that predicts the probability of each word in the vocabulary being a context word.

### 3. **Training Objective**
- The objective is to maximize the likelihood of predicting context words given the target word. The model uses techniques like negative sampling to improve efficiency during training.

### 4. **Working Mechanism**
1. **One-Hot Encoding**: The target word is converted into a one-hot encoded vector.
2. **Hidden Layer Calculation**: The input vector is multiplied by the weight matrix (input to hidden layer) to get the hidden layer representation:
   \[
   h = W_{input} \cdot x
   \]
   where \(x\) is the one-hot encoded vector and \(W_{input}\) is the weight matrix.
3. **Output Layer Calculation**: The hidden layer output is multiplied by the weight matrix (hidden to output layer) to predict probabilities for each word in the vocabulary:
   \[
   p = \text{softmax}(W_{output} \cdot h)
   \]
4. **Loss Calculation**: The model uses cross-entropy loss to measure the difference between predicted probabilities and actual context words.
5. **Backpropagation**: The weights are updated using gradient descent to minimize the loss.

### 5. **Example**
- Given the sentence: "The cat sits on the mat" with a context window size of 2:
  - **Target Word**: "sits"
  - **Predicted Context Words**: ["The", "cat", "on", "the"]
  
### 6. **Strengths**
- **Captures Semantic Relationships**: Skip-Gram is particularly effective at capturing relationships, especially for infrequent words.
- **Generates Rich Embeddings**: The embeddings learned can reflect various linguistic properties and similarities.

## Conclusion
The **Skip-Gram** model is a powerful technique for learning word representations, predicting context words from a target word, and providing valuable insights into word relationships and semantics in Natural Language Processing tasks.
