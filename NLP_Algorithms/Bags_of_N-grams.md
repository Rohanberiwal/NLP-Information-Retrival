# Bag of N-Grams in Natural Language Processing (NLP)

## Overview
The **Bag of N-Grams** is an extension of the **Bag of Words** (BoW) model in Natural Language Processing (NLP). While BoW treats each word as an independent token, the Bag of N-Grams model considers sequences of words, called "n-grams," to capture some of the context or structure in the text.

## What is an N-Gram?
An **n-gram** is a contiguous sequence of `n` items (words, characters, etc.) from a given text. For example:
- **Unigram (1-gram)**: single words (e.g., "The", "cat", "sat").
- **Bigram (2-gram)**: pairs of consecutive words (e.g., "The cat", "cat sat").
- **Trigram (3-gram)**: triplets of consecutive words (e.g., "The cat sat").

By using n-grams, the model can capture some of the word order and context, which is lost in a standard Bag of Words approach.

## How It Works

### 1. **Tokenization and N-Gram Generation**
The text is tokenized into words, and then sequences of `n` words (n-grams) are created.  
For example, the sentence:  
`"The cat sat on the mat."`

Using **bigrams (2-grams)**, the n-grams would be:  
`["The cat", "cat sat", "sat on", "on the", "the mat"]`.

### 2. **Vocabulary Creation**
A vocabulary is created from all the unique n-grams in the corpus. Each unique n-gram is added to the vocabulary, similar to how BoW builds a vocabulary from single words.

### 3. **Vectorization**
Each document is represented as a vector, where each element corresponds to the frequency of an n-gram in the document.  
For example, for two documents:
- Document 1: `"The cat sat on the mat."`
- Document 2: `"The dog sat on the mat."`

Using bigrams, the vocabulary would be:  
`["The cat", "cat sat", "sat on", "on the", "the mat", "The dog", "dog sat"]`.

The corresponding vectors would be:
- Document 1: `[1, 1, 1, 1, 1, 0, 0]`
- Document 2: `[0, 0, 1, 1, 1, 1, 1]`

### Example
For the sentence:  
`"I love to code."`

- **Unigrams**: `["I", "love", "to", "code"]`
- **Bigrams**: `["I love", "love to", "to code"]`
- **Trigrams**: `["I love to", "love to code"]`

After generating these n-grams, the model will count the frequency of each n-gram in the text and store it in the vector representation.

## Limitations
- **Increased dimensionality**: As `n` increases, the number of possible n-grams grows rapidly, leading to more sparse and higher-dimensional vectors.
- **Loss of long-term context**: N-grams capture local context but do not account for dependencies beyond `n` consecutive words.

## Use Cases
The **Bag of N-Grams** model is useful in:
- **Text classification** where word order and context are important (e.g., sentiment analysis).
- **Document similarity** where phrase-level comparison is necessary.
- **Information retrieval** to improve search engine results by considering word combinations.

## Installation
To implement the **Bag of N-Grams** model in Python, you can use `sklearn`’s `CountVectorizer`. Install the necessary libraries using:

```bash
pip install scikit-learn
