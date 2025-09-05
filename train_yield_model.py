import pandas as pd
import joblib
import time
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score

# --- Configuration ---
INPUT_CSV = "crop_yield.csv"
MODEL_FILE = "hackathon_yield_model.pkl"

# --- Hackathon Mode ---
# Set to True to train on a smaller sample for speed.
# 300k rows is a great balance of speed and accuracy.
USE_SAMPLE = True
SAMPLE_SIZE = 400000

print("--- Starting Model Training ---")
start_time = time.time()

# 1. Load Data
print(f"🔄 Loading dataset: {INPUT_CSV}...")
try:
    df = pd.read_csv(INPUT_CSV)
    print(f"✅ Successfully loaded {len(df)} rows.")
except FileNotFoundError:
    print(f"❌ ERROR: Dataset not found at '{INPUT_CSV}'. Please save your new data with this name.")
    exit()

if USE_SAMPLE:
    print(f"🔪 Using a random sample of {SAMPLE_SIZE} rows for fast training.")
    df = df.sample(n=SAMPLE_SIZE, random_state=42)

# 2. Define Features (X) and Target (y)
X = df.drop('Yield_tons_per_hectare', axis=1)
y = df['Yield_tons_per_hectare']

# 3. Preprocessing Setup
# We need to convert text columns (like 'Region', 'Soil_Type') into numbers.
categorical_features = ['Region', 'Soil_Type', 'Crop', 'Weather_Condition']
preprocessor = ColumnTransformer(
    transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)],
    remainder='passthrough'
)

# 4. Create Model Pipeline
# The pipeline bundles preprocessing and the model together.
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1, verbose=2))
])

# 5. Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Split data into {len(X_train)} training and {len(X_test)} testing samples.")

# 6. Train the Model
print("\n🔥 Training the RandomForest model... (This will take a few minutes)")
model_pipeline.fit(X_train, y_train)
print("\n✅ Training complete.")

# 7. Evaluate the Model
print("\n📈 Evaluating model performance...")
y_pred = model_pipeline.predict(X_test)
r2 = r2_score(y_test, y_pred)
print(f"⭐ Model R² score on test data: {r2:.4f}")

# 8. Save the Model
print(f"💾 Saving model pipeline to {MODEL_FILE}...")
joblib.dump(model_pipeline, MODEL_FILE)

end_time = time.time()
print(f"\n🎉 --- Success! Training finished in {end_time - start_time:.2f} seconds. ---")

