import torch
from transformers import BertTokenizer, BertForSequenceClassification
from datasets import load_dataset
from sklearn.metrics import accuracy_score, f1_score

dataset = load_dataset('glue', 'mrpc')
test_texts = dataset['validation']['sentence1']
test_labels = dataset['validation']['label']

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
test_encodings = tokenizer(test_texts, truncation=True, padding=True, max_length=512)

class NLPDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

test_dataset = NLPDataset(test_encodings, test_labels)
model = BertForSequenceClassification.from_pretrained('./results')
model.eval()

predictions = []
with torch.no_grad():
    for batch in torch.utils.data.DataLoader(test_dataset, batch_size=8):
        outputs = model(**{k: v.to(model.device) for k, v in batch.items()})
        logits = outputs.logits
        preds = torch.argmax(logits, dim=-1)
        predictions.extend(preds.cpu().numpy())

accuracy = accuracy_score(test_labels, predictions)
f1 = f1_score(test_labels, predictions)

print(f'Accuracy: {accuracy:.4f}')
print(f'F1 Score: {f1:.4f}')
