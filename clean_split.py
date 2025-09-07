import os
import shutil

data_dir = '/Users/swastiek/Desktop/KrishiMitra/data/plantvillage'
train_dir = os.path.join(data_dir, 'train')
val_dir = os.path.join(data_dir, 'val')

print("🧹 Cleaning old train/val folders...")

for d in [train_dir, val_dir]:
    if os.path.exists(d):
        shutil.rmtree(d)
        print(f"   ✅ Removed {d}")

print("✨ Clean complete. Now re-run train_disease_model.py to rebuild correctly.")
