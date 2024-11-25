import zipfile
import os
import random

import os
import random
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.preprocessing.image import ImageDataGenerator


def extract_zip(zip_path, extract_to_dir):
    if not os.path.exists(extract_to_dir):
        os.makedirs(extract_to_dir)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        print(f"Contents of the zip file: {zip_ref.namelist()}")
        zip_ref.extractall(extract_to_dir)
        print(f"Extracted all files to {extract_to_dir}")


import os
import shutil

def combine_images(src_folders, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for folder in src_folders:
        if not os.path.exists(folder):
            continue

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                dest_path = os.path.join(dest_folder, filename)
                counter = 1
                while os.path.exists(dest_path):
                    name, ext = os.path.splitext(filename)
                    dest_path = os.path.join(dest_folder, f"{name}_{counter}{ext}")
                    counter += 1

                shutil.copy(file_path, dest_path)


zip_file_path = '/content/archive.zip'
extract_dir = '/content/'
extract_zip(zip_file_path, extract_dir)

"""
src_folders = ['/content/colored_images/Mild' , '/content/colored_images/Moderate' ,'/content/colored_images/No_DR' ,'/content/colored_images/Proliferate_DR' ,'/content/colored_images/Severe']
dest_folder = '/content/Images'
"""

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
print(data)
print("The len of the data ", len(data))

split_index = int(0.8 * len(data))

train_data = data[:split_index]
val_data = data[split_index:]

print("Train Data:", train_data)
print("Validation Data:", val_data)
print("Length of train data:", len(train_data))
print("Length of validation data:", len(val_data))




def load_and_preprocess_data(data):
    images = []
    labels = []

    for item in data:
        img = load_img(item['image'], target_size=(224, 224))
        img_array = img_to_array(img) / 255.0
        images.append(img_array)
        labels.append(item['label'])

    return np.array(images), np.array(labels)

X_train, y_train = load_and_preprocess_data(train_data)
X_val, y_val = load_and_preprocess_data(val_data)

base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False

model = Model(inputs=base_model.input, outputs=base_model.output)

x = Flatten()(model.output)
x = Dense(128, activation='relu')(x)
x = Dropout(0.5)(x)
output = Dense(5, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=output)

model.compile(optimizer=Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
print(model)

early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

history = model.fit(
    X_train, y_train,
    epochs=200,
    batch_size=32,
    validation_data=(X_val, y_val),
    callbacks=[early_stopping]
)

val_loss, val_accuracy = model.evaluate(X_val, y_val)
print(f'Validation Loss: {val_loss}')
print(f'Validation Accuracy: {val_accuracy}')
