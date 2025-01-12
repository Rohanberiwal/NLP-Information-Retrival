import zipfile
import os
import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

zip_file_path = '/content/Food Ingredients and Recipe Dataset with Image Name Mapping.csv.zip'
extract_folder = '/content/food_ingredients_dataset'

os.makedirs(extract_folder, exist_ok=True)

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extract_folder)

extracted_files = os.listdir(extract_folder)
print("Extracted files:")
for file in extracted_files:
    print(file)

csv_file_path = os.path.join(extract_folder, extracted_files[0])
data = pd.read_csv(csv_file_path)

print(data.head())

def tokenize_ingredients(ingredients):
    ingredients_list = ast.literal_eval(ingredients)
    return [ingredient.strip() for ingredient in ingredients_list]

def check_null_values(dataframe):
    null_counts = dataframe.isnull().sum()
    null_summary = null_counts[null_counts > 0]
    if null_summary.empty:
        print("No null values found in the dataset.")
    else:
        print("Null values found in the following columns:")
        print(null_summary)

check_null_values(data)
data['Tokenized_Ingredients'] = data['Cleaned_Ingredients'].apply(tokenize_ingredients)

print(data[['Title', 'Tokenized_Ingredients']].head())
vectorizer = TfidfVectorizer()
ingredient_vectors = vectorizer.fit_transform(data['Tokenized_Ingredients'].apply(lambda x: ' '.join(x)))

cosine_similarity_matrix = cosine_similarity(ingredient_vectors)
print("Cosine Similarity Matrix:")
print(cosine_similarity_matrix)


import spacy
nlp = spacy.load("en_core_web_sm")

def extract_named_entities(ingredients):
    entities = []
    for ingredient in ingredients:
        doc = nlp(ingredient)
        entities.extend([(ent.text, ent.label_) for ent in doc.ents])
    return entities
data['Named_Entities'] = data['Tokenized_Ingredients'].apply(extract_named_entities)
print(data[['Title', 'Named_Entities']].head())
