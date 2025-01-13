import os
import zipfile
import random
import numpy as np
import tensorflow as tf
from sklearn.model_selection import KFold
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications import ResNet152
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

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

alpha_values = [0.01, 0.05, 0.1]

test_results = {}

for alpha in alpha_values:
    print(f"\nTesting at alpha = {alpha}")
    
    rejection_count = 0
    alpha_test_results = {}

    shapiro_test = stats.shapiro(y_train)
    shapiro_reject_null = shapiro_test.pvalue < alpha
    alpha_test_results['Shapiro-Wilk'] = (shapiro_reject_null, shapiro_test)
    if shapiro_reject_null:
        rejection_count += 1

    ks_test = stats.kstest(y_train, 'norm')
    ks_reject_null = ks_test.pvalue < alpha
    alpha_test_results['Kolmogorov-Smirnov'] = (ks_reject_null, ks_test)
    if ks_reject_null:
        rejection_count += 1

    mild_data = y_train[y_train == 1]
    moderate_data = y_train[y_train == 2]
    t_test = stats.ttest_ind(mild_data, moderate_data)
    t_test_reject_null = t_test.pvalue < alpha
    alpha_test_results['T-test (Mild vs Moderate)'] = (t_test_reject_null, t_test)
    if t_test_reject_null:
        rejection_count += 1

    anova_test = stats.f_oneway(
        y_train[y_train == 0],
        y_train[y_train == 1],
        y_train[y_train == 2],
        y_train[y_train == 3],
        y_train[y_train == 4]
    )
    anova_reject_null = anova_test.pvalue < alpha
    alpha_test_results['ANOVA'] = (anova_reject_null, anova_test)
    if anova_reject_null:
        rejection_count += 1

    chi2, p_val = stats.chisquare(np.bincount(y_train))
    chi2_reject_null = p_val < alpha
    alpha_test_results['Chi-square'] = (chi2_reject_null, (chi2, p_val))
    if chi2_reject_null:
        rejection_count += 1

    mann_whitney_test = stats.mannwhitneyu(mild_data, moderate_data)
    mann_whitney_reject_null = mann_whitney_test.pvalue < alpha
    alpha_test_results['Mann-Whitney U Test'] = (mann_whitney_reject_null, mann_whitney_test)
    if mann_whitney_reject_null:
        rejection_count += 1

    kruskal_test = stats.kruskal(
        y_train[y_train == 0],
        y_train[y_train == 1],
        y_train[y_train == 2],
        y_train[y_train == 3],
        y_train[y_train == 4]
    )
    kruskal_reject_null = kruskal_test.pvalue < alpha
    alpha_test_results['Kruskal-Wallis'] = (kruskal_reject_null, kruskal_test)
    if kruskal_reject_null:
        rejection_count += 1

    test_results[alpha] = {'rejection_count': rejection_count, 'results': alpha_test_results}

optimal_alpha = max(test_results, key=lambda alpha: test_results[alpha]['rejection_count'])
print(f"\nOptimal alpha is: {optimal_alpha} with {test_results[optimal_alpha]['rejection_count']} rejections")

print("\nResults for Optimal Alpha:")
for test_name, (reject, test_output) in test_results[optimal_alpha]['results'].items():
    decision = "Reject" if reject else "Fail to Reject"
    p_value = test_output[1] if isinstance(test_output, tuple) else test_output.pvalue
    print(f"{test_name}: {decision} (p-value = {p_value})")
