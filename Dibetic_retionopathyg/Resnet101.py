import os
import zipfile
import random
import numpy as np
import tensorflow as tf
from sklearn.model_selection import KFold
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications import ResNet101
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt

def extract_zip(zip_path, extract_to_dir):
    if not os.path.exists(extract_to_dir):
        os.makedirs(extract_to_dir)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_dir)

def load_and_preprocess_data(data):
    images = []
    labels = []
    for item in data:
        img = load_img(item['image'], target_size=(224, 224))
        img_array = img_to_array(img) / 255.0
        images.append(img_array)
        labels.append(item['label'])
    return np.array(images), np.array(labels)

zip_file_path = '/content/archive.zip'
extract_dir = '/content/'
extract_zip(zip_file_path, extract_dir)

src_folders = [
    '/content/colored_images/Mild',
    '/content/colored_images/Moderate',
    '/content/colored_images/No_DR',
    '/content/colored_images/Proliferate_DR',
    '/content/colored_images/Severe'
]

labels = {
    '/content/colored_images/No_DR': 0,
    '/content/colored_images/Mild': 1,
    '/content/colored_images/Moderate': 2,
    '/content/colored_images/Severe': 3,
    '/content/colored_images/Proliferate_DR': 4
}

data = []
for folder in src_folders:
    label = labels[folder]
    for filename in os.listdir(folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(folder, filename)
            data.append({'image': image_path, 'label': label})

random.shuffle(data)

split_index = int(0.8 * len(data))
train_data = data[:split_index]
val_data = data[split_index:]

X_train, y_train = load_and_preprocess_data(train_data)
X_val, y_val = load_and_preprocess_data(val_data)

base_model = ResNet101(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False

x = Flatten()(base_model.output)
x = Dense(128, activation='relu')(x)
x = Dropout(0.5)(x)
output = Dense(5, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=output)

model.compile(optimizer=Adam(clipvalue=1.0), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

kf = KFold(n_splits=5, shuffle=True, random_state=42)

train_accuracies = []
val_accuracies = []
train_losses = []
val_losses = []

for fold, (train_index, val_index) in enumerate(kf.split(X_train, y_train)):
    X_train_fold, X_val_fold = X_train[train_index], X_train[val_index]
    y_train_fold, y_val_fold = y_train[train_index], y_train[val_index]

    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    history = model.fit(
        X_train_fold, y_train_fold,
        epochs=40,
        batch_size=32,
        validation_data=(X_val_fold, y_val_fold),
        callbacks=[early_stopping]
    )

    train_accuracies.append(history.history['accuracy'])
    val_accuracies.append(history.history['val_accuracy'])
    train_losses.append(history.history['loss'])
    val_losses.append(history.history['val_loss'])

train_accuracy_avg = np.mean(train_accuracies, axis=0)
val_accuracy_avg = np.mean(val_accuracies, axis=0)
train_loss_avg = np.mean(train_losses, axis=0)
val_loss_avg = np.mean(val_losses, axis=0)

plt.figure(figsize=(12, 6))
plt.plot(train_accuracy_avg, label='Train Accuracy')
plt.plot(val_accuracy_avg, label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('Training and Validation Accuracy during Cross-Validation')
plt.legend()
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(train_loss_avg, label='Train Loss')
plt.plot(val_loss_avg, label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Training and Validation Loss during Cross-Validation')
plt.legend()
plt.show()

val_loss, val_accuracy = model.evaluate(X_val, y_val)
print(f'Final Validation Loss: {val_loss}')
print(f'Final Validation Accuracy: {val_accuracy}')


import seaborn as sns
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

plt.figure(figsize=(10, 5))
sns.boxplot(y=y_train)
plt.title('Boxplot for Label Distribution (Outliers Detection)')
plt.ylabel('Labels')
plt.show()

plt.figure(figsize=(10, 5))
plt.scatter(range(len(y_train)), y_train, alpha=0.6)
plt.title('Scatter Plot of Labels')
plt.xlabel('Index')
plt.ylabel('Labels')
plt.show()

quantiles = np.quantile(y_train, [0.25, 0.5, 0.75])
plt.figure(figsize=(10, 5))
plt.plot([0.25, 0.5, 0.75], quantiles, marker='o')
plt.title('Quantile Plot')
plt.xlabel('Quantiles (25%, 50%, 75%)')
plt.ylabel('Values')
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(train_accuracy_avg, label='Train Accuracy')
plt.plot(val_accuracy_avg, label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('Training and Validation Accuracy during Cross-Validation')
plt.legend()
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(train_loss_avg, label='Train Loss')
plt.plot(val_loss_avg, label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Training and Validation Loss during Cross-Validation')
plt.legend()
plt.show()


val_predictions = np.argmax(model.predict(X_val), axis=1)
conf_matrix = confusion_matrix(y_val, val_predictions)
cm_display = ConfusionMatrixDisplay(conf_matrix, display_labels=list(labels.values()))

plt.figure(figsize=(10, 7))
cm_display.plot(cmap='Blues', values_format='d')
plt.title('Confusion Matrix')
plt.show()
