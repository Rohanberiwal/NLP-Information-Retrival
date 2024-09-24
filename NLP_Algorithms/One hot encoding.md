# One-Hot Encoding in Machine Learning

## Overview
**One-Hot Encoding** is a technique used to convert categorical data into a numerical format that can be used by machine learning algorithms. It creates binary columns for each unique category in the dataset and assigns a `1` to the relevant category and `0` to all others.

## How It Works

### 1. **Categorical Data**
In many datasets, features may contain categorical values (e.g., "Red", "Green", "Blue"). Machine learning models cannot work with these text labels directly, so they must be transformed into a numerical format.

### 2. **Creating Binary Vectors**
One-Hot Encoding converts each category into a binary vector. For example, suppose you have a feature called "Color" with the following values:  
`["Red", "Green", "Blue"]`.

One-Hot Encoding will transform these values into the following binary vectors:
- Red: `[1, 0, 0]`
- Green: `[0, 1, 0]`
- Blue: `[0, 0, 1]`

Each position in the vector corresponds to one possible category, and the `1` indicates the presence of that category in the data.

### Example
Consider a dataset with a "Color" column:
```text
Color
------
Red
Green
Blue
Red
