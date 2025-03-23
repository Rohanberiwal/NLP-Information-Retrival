import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
import torchvision.transforms as transforms
from torchvision.transforms import RandomApply, RandomChoice, RandomRotation, RandomHorizontalFlip, RandomVerticalFlip, RandomAffine, RandomGrayscale

# Function to generate random matrices
def generate_random_matrices(num_samples, img_size=32):
    electrons_hit_energy = np.random.rand(num_samples, img_size, img_size)
    electrons_time = np.random.rand(num_samples, img_size, img_size)
    
    photons_hit_energy = np.random.rand(num_samples, img_size, img_size)
    photons_time = np.random.rand(num_samples, img_size, img_size)
    
    return electrons_hit_energy, electrons_time, photons_hit_energy, photons_time

num_datasets = 1000  
num_samples_per_dataset = 1
all_electrons_hit_energy = []
all_electrons_time = []
all_photons_hit_energy = []
all_photons_time = []

for _ in range(num_datasets):
    electrons_hit_energy, electrons_time, photons_hit_energy, photons_time = generate_random_matrices(num_samples_per_dataset)
    all_electrons_hit_energy.append(electrons_hit_energy)
    all_electrons_time.append(electrons_time)
    all_photons_hit_energy.append(photons_hit_energy)
    all_photons_time.append(photons_time)

# Convert lists to numpy arrays
all_electrons_hit_energy = np.array(all_electrons_hit_energy)
all_electrons_time = np.array(all_electrons_time)
all_photons_hit_energy = np.array(all_photons_hit_energy)
all_photons_time = np.array(all_photons_time)

# Data division
num_total_datasets = len(all_electrons_hit_energy)
num_train = int(0.8 * num_total_datasets)
num_val = int(0.1 * num_total_datasets)
num_test = num_total_datasets - num_train - num_val

# Split into training, validation, and test sets
train_electrons_hit_energy = all_electrons_hit_energy[:num_train]
train_electrons_time = all_electrons_time[:num_train]
train_photons_hit_energy = all_photons_hit_energy[:num_train]
train_photons_time = all_photons_time[:num_train]

val_electrons_hit_energy = all_electrons_hit_energy[num_train:num_train+num_val]
val_electrons_time = all_electrons_time[num_train:num_train+num_val]
val_photons_hit_energy = all_photons_hit_energy[num_train:num_train+num_val]
val_photons_time = all_photons_time[num_train:num_train+num_val]

test_electrons_hit_energy = all_electrons_hit_energy[num_train+num_val:]
test_electrons_time = all_electrons_time[num_train+num_val:]
test_photons_hit_energy = all_photons_hit_energy[num_train+num_val:]
test_photons_time = all_photons_time[num_train+num_val:]

# Convert data to PyTorch tensors
train_electrons_hit_energy_tensor = torch.FloatTensor(train_electrons_hit_energy)
train_electrons_time_tensor = torch.FloatTensor(train_electrons_time)
train_photons_hit_energy_tensor = torch.FloatTensor(train_photons_hit_energy)
train_photons_time_tensor = torch.FloatTensor(train_photons_time)

val_electrons_hit_energy_tensor = torch.FloatTensor(val_electrons_hit_energy)
val_electrons_time_tensor = torch.FloatTensor(val_electrons_time)
val_photons_hit_energy_tensor = torch.FloatTensor(val_photons_hit_energy)
val_photons_time_tensor = torch.FloatTensor(val_photons_time)

test_electrons_hit_energy_tensor = torch.FloatTensor(test_electrons_hit_energy)
test_electrons_time_tensor = torch.FloatTensor(test_electrons_time)
test_photons_hit_energy_tensor = torch.FloatTensor(test_photons_hit_energy)
test_photons_time_tensor = torch.FloatTensor(test_photons_time)

# Concatenate hit energy and time matrices along the channel dimension
train_electrons_data = torch.stack((train_electrons_hit_energy_tensor, train_electrons_time_tensor), dim=1)
train_photons_data = torch.stack((train_photons_hit_energy_tensor, train_photons_time_tensor), dim=1)

val_electrons_data = torch.stack((val_electrons_hit_energy_tensor, val_electrons_time_tensor), dim=1)
val_photons_data = torch.stack((val_photons_hit_energy_tensor, val_photons_time_tensor), dim=1)

test_electrons_data = torch.stack((test_electrons_hit_energy_tensor, test_electrons_time_tensor), dim=1)
test_photons_data = torch.stack((test_photons_hit_energy_tensor, test_photons_time_tensor), dim=1)
train_data = torch.cat((train_electrons_data, train_photons_data), dim=0)
val_data = torch.cat((val_electrons_data, val_photons_data), dim=0)
test_data = torch.cat((test_electrons_data, test_photons_data), dim=0)

train_labels = torch.cat((torch.zeros(train_electrons_data.size(0)), torch.ones(train_photons_data.size(0))))
val_labels = torch.cat((torch.zeros(val_electrons_data.size(0)), torch.ones(val_photons_data.size(0))))
test_labels = torch.cat((torch.zeros(test_electrons_data.size(0)), torch.ones(test_photons_data.size(0))))

from torch.utils.data import Dataset, DataLoader
class AugmentedDataset(Dataset):
    def __init__(self, data, labels, transform=None):
        self.data = data
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        image = self.data[idx]
        label = self.labels[idx]
        if self.transform:
            image = self.transform(image)
        return image, label

transformations = transforms.Compose([
    RandomApply([RandomChoice([
        RandomRotation(15),
        RandomHorizontalFlip(),
        RandomVerticalFlip(),
        RandomAffine(degrees=0, translate=(0.1, 0.1)),
        RandomGrayscale(p=0.1)
    ])], p=0.8)
])

train_dataset = AugmentedDataset(train_data, train_labels, transform=transformations)
val_dataset = AugmentedDataset(val_data, val_labels, transform=None)
test_dataset = AugmentedDataset(test_data, test_labels, transform=None)

batch_size = 32
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)


class ResNet15(nn.Module):
    def __init__(self):
        super(ResNet15, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=2, out_channels=64, kernel_size=3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(128)
        
        self.fc = nn.Linear(128 * 8 * 8, 2)  # Assuming 32x32 input size and 2 output classes
    
    def forward(self, x):
        # Reshape input to remove the extra dimension if present
        if x.dim() == 5:
            x = x.squeeze(2)  # Remove the extra dimension
        
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)
        
        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu(x)
        x = self.maxpool(x)
        
        x = torch.flatten(x, 1)
        x = self.fc(x)
        
        return x


model = ResNet15()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-5) 
optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-5)


lambda_l1 = 1e-4 
def l1_regularization(model, lambda_l1):
    l1_loss = 0
    for param in model.parameters():
        l1_loss += torch.sum(torch.abs(param))
    return lambda_l1 * l1_loss

num_epochs = 100
train_losses = []
train_accuracies = []
val_losses = []
val_accuracies = []
for epoch in range(num_epochs):
    train_loss = 0.0
    train_correct = 0
    total_train = 0
    
    model.train()
    for inputs, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels.long())
        l1_loss = l1_regularization(model, lambda_l1)
        total_loss = loss + l1_loss
        
        total_loss.backward()
        optimizer.step()
        
        train_loss += total_loss.item()
        _, predicted = torch.max(outputs, 1)
        total_train += labels.size(0)
        train_correct += (predicted == labels).sum().item()
    
    train_losses.append(train_loss / len(train_loader))
    train_accuracies.append(train_correct / total_train)
    
    val_loss = 0.0
    val_correct = 0
    total_val = 0
    
    model.eval()
    with torch.no_grad():
        for inputs, labels in val_loader:
            outputs = model(inputs)
            loss = criterion(outputs, labels.long())
            val_loss += loss.item()
            _, predicted = torch.max(outputs, 1)
            total_val += labels.size(0)
            val_correct += (predicted == labels).sum().item()
    
    val_losses.append(val_loss / len(val_loader))
    val_accuracies.append(val_correct / total_val)
    
    print(f"Epoch [{epoch+1}/{num_epochs}], Train Loss: {train_losses[-1]:.4f}, Train Accuracy: {train_accuracies[-1]:.4f}, Val Loss: {val_losses[-1]:.4f}, Val Accuracy: {val_accuracies[-1]:.4f}")

torch.save(model.state_dict(), 'resnet15_finetuned.pth')

# Plot training loss and validation accuracy
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(range(num_epochs), train_losses, label='Train Loss')
plt.plot(range(num_epochs), val_losses, label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(range(num_epochs), train_accuracies, label='Train Accuracy')
plt.plot(range(num_epochs), val_accuracies, label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

plt.show()
# Evaluate on test data
model.eval()
test_correct = 0
total_test = 0
test_predictions = []
test_targets = []

with torch.no_grad():
    for inputs, labels in test_loader:
        outputs = model(inputs)
        _, predicted = torch.max(outputs, 1)
        
        total_test += labels.size(0)
        test_correct += (predicted == labels).sum().item()
        
        test_predictions.extend(predicted.cpu().numpy())
        test_targets.extend(labels.cpu().numpy())

test_accuracy = test_correct / total_test
print(f'Test Accuracy: {test_accuracy:.4f}')
from sklearn.metrics import classification_report, confusion_matrix

print("Confusion Matrix:")
print(confusion_matrix(test_targets, test_predictions))
print("\nClassification Report:")
print(classification_report(test_targets, test_predictions, target_names=["Electron", "Photon"]))
print("This is the code for the Testing ")
import random
def generate_random_test_cases(num_cases, img_size=32):
    test_cases = []
    labels = []
    for _ in range(num_cases):
        is_photon = random.choice([True, False])
        
        if is_photon:
            photons_hit_energy = np.random.rand(img_size, img_size)
            photons_time = np.random.rand(img_size, img_size)
            test_cases.append(np.stack((photons_hit_energy, photons_time), axis=0))
            labels.append(1)  
        else:
            electrons_hit_energy = np.random.rand(img_size, img_size)
            electrons_time = np.random.rand(img_size, img_size)
            test_cases.append(np.stack((electrons_hit_energy, electrons_time), axis=0))
            labels.append(0) 
    return np.array(test_cases), np.array(labels)

num_test_cases = 10
test_inputs, test_labels = generate_random_test_cases(num_test_cases)

test_inputs_tensor = torch.FloatTensor(test_inputs)

model.eval()
with torch.no_grad():
    outputs = model(test_inputs_tensor)
    _, predicted = torch.max(outputs, 1)

predicted_labels = predicted.cpu().numpy()
for i in range(num_test_cases):
    particle_type = "Photon" if predicted_labels[i] == 1 else "Electron"
    true_type = "Photon" if test_labels[i] == 1 else "Electron"
    print(f"Test Case {i+1}: Predicted: {particle_type}, True Label: {true_type}")

print("The code ends here ")