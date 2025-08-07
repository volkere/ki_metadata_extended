"""
TensorFlow/Keras Training Script for Age and Gender Prediction

Usage:
  - Prepare your dataset as described in the README (see dataset structure)
  - Adjust paths, batch size, epochs, and model as needed
  - Run: python train_age_gender_keras.py
  - Output: age_gender_model_keras.h5

Requirements:
  - tensorflow, pandas, scikit-learn, pillow
"""
import os
import pandas as pd
import numpy as np
from tensorflow.keras.utils import Sequence
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import LabelEncoder

# --- Dataset Generator ---
class AgeGenderSequence(Sequence):
    def __init__(self, csv_file, img_dir, batch_size=32, img_size=(256, 256)):
        self.labels = pd.read_csv(csv_file)
        self.img_dir = img_dir
        self.batch_size = batch_size
        self.img_size = img_size
        self.gender_encoder = LabelEncoder()
        self.labels['gender'] = self.gender_encoder.fit_transform(self.labels['gender'])

    def __len__(self):
        return int(np.ceil(len(self.labels) / self.batch_size))

    def __getitem__(self, idx):
        batch = self.labels.iloc[idx * self.batch_size:(idx + 1) * self.batch_size]
        images = []
        ages = []
        genders = []
        for _, row in batch.iterrows():
            img_path = os.path.join(self.img_dir, row[0])
            img = load_img(img_path, target_size=self.img_size)
            img = img_to_array(img) / 255.0
            images.append(img)
            ages.append(row[1])
            genders.append(row[2])
        return np.array(images), [np.array(ages), np.array(genders)]

# --- Simple CNN Model ---
input_layer = Input(shape=(256, 256, 3))
x = Conv2D(16, 3, padding='same', activation='relu')(input_layer)
x = MaxPooling2D(2)(x)
x = Conv2D(32, 3, padding='same', activation='relu')(x)
x = MaxPooling2D(2)(x)
x = Conv2D(64, 3, padding='same', activation='relu')(x)
x = MaxPooling2D(2)(x)
x = Flatten()(x)
x = Dropout(0.5)(x)

age_output = Dense(1, name='age')(x)  # Regression
gender_output = Dense(2, activation='softmax', name='gender')(x)  # Classification

model = Model(inputs=input_layer, outputs=[age_output, gender_output])
model.compile(
    optimizer=Adam(1e-3),
    loss={'age': 'mse', 'gender': 'sparse_categorical_crossentropy'},
    metrics={'age': 'mae', 'gender': 'accuracy'}
)

# --- Data Generators ---
train_seq = AgeGenderSequence('dataset/train/labels.csv', 'dataset/train/images')
val_seq = AgeGenderSequence('dataset/val/labels.csv', 'dataset/val/images')

# --- Training ---
model.fit(
    train_seq,
    validation_data=val_seq,
    epochs=10
)

# --- Save Model ---
model.save('age_gender_model_keras.h5')