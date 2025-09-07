import os
import shutil
import random
import torch
from torchvision import datasets, transforms, models
from torch import nn, optim
from tqdm import tqdm, trange

# ==========================
# 0. Parameters
# ==========================
BASE_DATA_DIR = '/Users/swastiek/Desktop/KrishiMitra/data/plantvillage'
MAX_IMAGES_PER_CLASS = 200   # limit images per class
IMAGE_SIZE = 128             # smaller images for CPU
BATCH_SIZE = 32
NUM_WORKERS = 0              # important for macOS CPU
EPOCHS = 3

# ==========================
# 1. Helper functions
# ==========================
def prepare_dataset():
    """Split dataset into train/val and limit images per class."""
    # Detect wrapper folder
    subdirs = [d for d in os.listdir(BASE_DATA_DIR) if os.path.isdir(os.path.join(BASE_DATA_DIR, d))]
    if len(subdirs) == 1 and subdirs[0].lower().startswith("plantvillage"):
        print(f"📂 Found wrapper folder '{subdirs[0]}', using it as dataset root.")
        data_dir = os.path.join(BASE_DATA_DIR, subdirs[0])
    else:
        data_dir = BASE_DATA_DIR

    train_dir = os.path.join(data_dir, 'train')
    val_dir = os.path.join(data_dir, 'val')

    # Remove old train/val
    for d in [train_dir, val_dir]:
        if os.path.exists(d):
            shutil.rmtree(d)
    os.makedirs(train_dir)
    os.makedirs(val_dir)

    total_train, total_val = 0, 0

    for class_name in os.listdir(data_dir):
        class_path = os.path.join(data_dir, class_name)
        if os.path.isdir(class_path) and class_name not in ['train', 'val']:
            print(f"\n📂 Processing class: {class_name}")
            images = [img for img in os.listdir(class_path) if os.path.isfile(os.path.join(class_path, img))]
            if len(images) == 0:
                print(f"⚠️ Skipping {class_name} (no images found).")
                continue

            random.shuffle(images)
            images = images[:MAX_IMAGES_PER_CLASS]  # limit per class
            split_idx = int(0.8 * len(images))
            train_images = images[:split_idx]
            val_images = images[split_idx:]

            train_class_dir = os.path.join(train_dir, class_name)
            val_class_dir = os.path.join(val_dir, class_name)
            os.makedirs(train_class_dir, exist_ok=True)
            os.makedirs(val_class_dir, exist_ok=True)

            for img in train_images:
                shutil.copy(os.path.join(class_path, img), os.path.join(train_class_dir, img))
            for img in val_images:
                shutil.copy(os.path.join(class_path, img), os.path.join(val_class_dir, img))

            print(f"   ✅ {len(train_images)} train, {len(val_images)} val images")
            total_train += len(train_images)
            total_val += len(val_images)

    print(f"\n🎉 Dataset ready! Total train: {total_train}, val: {total_val}")
    return train_dir, val_dir

# ==========================
# 2. Main training
# ==========================
if __name__ == "__main__":
    # Prepare dataset
    train_dir, val_dir = prepare_dataset()

    # Data transforms
    data_transforms = {
        'train': transforms.Compose([
            transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
        ]),
        'val': transforms.Compose([
            transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
            transforms.ToTensor(),
        ]),
    }

    # Datasets and loaders
    print("\n📂 Loading datasets...")
    image_datasets = {
        'train': datasets.ImageFolder(train_dir, data_transforms['train']),
        'val': datasets.ImageFolder(val_dir, data_transforms['val'])
    }
    dataloaders = {
        'train': torch.utils.data.DataLoader(image_datasets['train'], batch_size=BATCH_SIZE, shuffle=True, num_workers=NUM_WORKERS),
        'val': torch.utils.data.DataLoader(image_datasets['val'], batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS)
    }
    class_names = image_datasets['train'].classes
    print(f"✅ Classes: {class_names}")
    print(f"📊 Train samples: {len(image_datasets['train'])}, Val samples: {len(image_datasets['val'])}")

    # Model setup
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"⚡ Training on device: {device}")
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, len(class_names))
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Training loop
    best_acc = 0.0
    for epoch in trange(EPOCHS, desc="Epochs"):
        print(f"\n📌 Epoch {epoch+1}/{EPOCHS}")

        # Training
        model.train()
        running_loss = 0.0
        for inputs, labels in tqdm(dataloaders['train'], desc="Training Batches", leave=False):
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * inputs.size(0)
        epoch_loss = running_loss / len(image_datasets['train'])
        print(f"📉 Train Loss: {epoch_loss:.4f}")

        # Validation
        model.eval()
        correct, total = 0, 0
        for inputs, labels in tqdm(dataloaders['val'], desc="Validation Batches", leave=False):
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)
        acc = correct / total
        print(f"🎯 Validation Accuracy: {acc:.4f}")

        # Save best model
        if acc > best_acc:
            best_acc = acc
            torch.save({'model_state_dict': model.state_dict(), 'class_names': class_names}, 'plant_disease_model_fast.pth')
            print("💾 Best model saved!")

    print(f"\n🏆 Training complete. Best validation accuracy: {best_acc:.4f}")
