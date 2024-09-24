# Feedforward Neural Networks and Attention Mechanisms

## Overview of Feedforward Neural Networks (FNNs)

### What is a Feedforward Neural Network?
A feedforward neural network (FNN) is a type of artificial neural network where connections between nodes do not form cycles. Information flows in one direction, from input to output.

### Structure of FNNs
1. **Input Layer**: Accepts input features.
2. **Hidden Layers**: Contains neurons that apply weights, biases, and activation functions to the inputs. The complexity can vary with the number of layers and neurons.
3. **Output Layer**: Produces the final output, either as a single value (regression) or a probability distribution (classification).

### Working of FNNs
- **Weighted Sum Calculation**:
  \[
  z = W \cdot x + b
  \]
  - Where \( W \) is the weight matrix, \( x \) is the input vector, and \( b \) is the bias.
  
- **Activation Function**:
  \[
  a = \text{activation}(z)
  \]
  - Applies non-linearity to the weighted sum (e.g., ReLU, sigmoid, or tanh).

- **Forward Pass**: Information propagates from input to output layer without feedback loops.

### Purpose
FNNs are utilized in various tasks, including classification and regression, to learn complex mappings from inputs to outputs based on training data.

---

## Integration of Attention in Neural Networks

### Role of Attention
Attention mechanisms enhance the performance of traditional feedforward networks by allowing them to focus on specific parts of the input data, which is essential in sequential or structured data tasks like NLP.

### How Attention Works with FNNs
1. **Contextualization**: Attention creates context vectors summarizing relevant input information based on the current focus (query).

2. **Multi-Head Attention**:
   - Multiple linear transformations generate different queries, keys, and values, allowing the model to learn various input representations.
   - Each attention head computes its output independently.
   - The outputs from all heads are concatenated and passed through a feedforward neural network for effective information combination.

3. **Feedforward Layers After Attention**: The output of the attention mechanism is fed into a feedforward network, which transforms the data further through non-linear mappings, capturing complex relationships.

### Benefits of Combining Attention with FNNs
- **Improved Contextual Understanding**: Attention allows models to focus on relevant parts of the input, enhancing context comprehension and overall performance in tasks like language modeling.
