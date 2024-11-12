from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset

model_name = "dmis-lab/biobert-v1.1"
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)  # Adjust num_labels
tokenizer = AutoTokenizer.from_pretrained(model_name)
print(model)
