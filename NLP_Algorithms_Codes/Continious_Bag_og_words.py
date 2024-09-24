import numpy as np

class CBOW:
    def __init__(self, vocab_size, embedding_dim):
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.W1 = np.random.rand(vocab_size, embedding_dim)  # Weight matrix for input to hidden layer
        self.W2 = np.random.rand(embedding_dim, vocab_size)  # Weight matrix for hidden to output layer

    def softmax(self, x):
        e_x = np.exp(x - np.max(x))  # Stability improvement
        return e_x / e_x.sum(axis=0)

    def train(self, context_words, target_word, learning_rate=0.01):
        # One-hot encoding for context words and target word
        context_vector = np.zeros(self.vocab_size)
        for word in context_words:
            context_vector[word] += 1
        target_vector = np.zeros(self.vocab_size)
        target_vector[target_word] = 1

        # Forward pass
        hidden_layer = np.mean(self.W1[context_words], axis=0)
        output_layer = np.dot(hidden_layer, self.W2)
        predicted_probs = self.softmax(output_layer)

        # Backpropagation
        error = predicted_probs - target_vector
        self.W2 -= learning_rate * np.outer(hidden_layer, error)
        for word in context_words:
            self.W1[word] -= learning_rate * error.dot(self.W2.T)

# Example usage
vocab_size = 10  # Example vocabulary size
embedding_dim = 5  # Example embedding dimension
cbow_model = CBOW(vocab_size, embedding_dim)

# Train with example context and target word
context_words = [0, 1, 2]  # Example context word indices
target_word = 3  # Example target word index
cbow_model.train(context_words, target_word)
