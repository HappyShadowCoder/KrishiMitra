import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# --- Configuration ---
INPUT_CSV = "crop_yield.csv"
MODEL_FILE = "hackathon_yield_model.pkl"

# --- Evaluate the Model's Accuracy ---
print("--- Starting Model Accuracy Check ---")

# 1. Load Data
try:
    df = pd.read_csv(INPUT_CSV)
    print("✅ Dataset loaded successfully.")
except FileNotFoundError:
    print(f"❌ ERROR: Dataset not found at '{INPUT_CSV}'. Please provide the correct data file.")
    exit()

# 2. Load the trained model
try:
    model_pipeline = joblib.load(MODEL_FILE)
    print("✅ Trained model loaded successfully.")
except FileNotFoundError:
    print(f"❌ ERROR: Model file not found at '{MODEL_FILE}'. Please run the full training script first.")
    exit()

# 3. Define Features (X) and Target (y)
X = df.drop('Yield_tons_per_hectare', axis=1)
y = df['Yield_tons_per_hectare']

# 4. Split Data (using the same split as training for consistent evaluation)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Evaluate the Model
print("📈 Evaluating model performance...")
y_pred = model_pipeline.predict(X_test)
r2 = r2_score(y_test, y_pred)

# 6. Print Accuracy
print(f"⭐ Model R² score (accuracy): {r2:.4f}")
