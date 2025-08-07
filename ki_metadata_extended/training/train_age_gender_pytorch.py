"""
PyTorch Training Script for Age and Gender Prediction

Usage:
  - Prepare your dataset as described in the README (see dataset structure)
  - Adjust paths, batch size, epochs, and model as needed
  - Run: python train_age_gender_pytorch.py
  - Output: age_gender_model.pth

Requirements:
  - torch, torchvision, pandas, scikit-learn, pillow
"""
import os
import pandas as pd
from PIL import Image
from torch.utils.data import Dataset, DataLoader
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from sklearn.preprocessing import LabelEncoder

# --- Dataset Class ---
class AgeGenderDataset(Dataset):
    def __init__(self, csv_file, img_dir, transform=None):
        self.labels = pd.read_csv(csv_file)
        self.img_dir = img_dir
        self.transform = transform
        self.gender_encoder = LabelEncoder()
        self.labels['gender'] = self.gender_encoder.fit_transform(self.labels['gender'])

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.labels.iloc[idx, 0])
        image = Image.open(img_path).convert('RGB')
        age = torch.tensor(self.labels.iloc[idx, 1], dtype=torch.float32)
        gender = torch.tensor(self.labels.iloc[idx, 2], dtype=torch.long)
        if self.transform:
            image = self.transform(image)
        return image, age, gender

# --- Simple CNN Model ---
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2)
        )
        self.flatten = nn.Flatten()
        self.fc_age = nn.Linear(64 * 32 * 32, 1)      # For age regression
        self.fc_gender = nn.Linear(64 * 32 * 32, 2)   # For gender classification

    def forward(self, x):
        x = self.features(x)
        x = self.flatten(x)
        age = self.fc_age(x).squeeze(1)
        gender = self.fc_gender(x)
        return age, gender

# --- Training Setup ---
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
])

train_dataset = AgeGenderDataset('dataset/train/labels.csv', 'dataset/train/images', transform)
val_dataset = AgeGenderDataset('dataset/val/labels.csv', 'dataset/val/images', transform)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32)

model = SimpleCNN().to(device)
criterion_age = nn.MSELoss()
criterion_gender = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

# --- Training Loop ---
for epoch in range(10):
    model.train()
    for images, ages, genders in train_loader:
        images, ages, genders = images.to(device), ages.to(device), genders.to(device)
        optimizer.zero_grad()
        pred_ages, pred_genders = model(images)
        loss_age = criterion_age(pred_ages, ages)
        loss_gender = criterion_gender(pred_genders, genders)
        loss = loss_age + loss_gender
        loss.backward()
        optimizer.step()
    print(f'Epoch {epoch+1}, Loss: {loss.item():.4f}')

# --- Save Model ---
torch.save(model.state_dict(), 'age_gender_model.pth')