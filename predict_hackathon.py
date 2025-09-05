import joblib
import pandas as pd

# Load the trained model pipeline from the file.
# This happens once when the server starts.
MODEL_FILE = "hackathon_yield_model.pkl"
try:
    model_pipeline = joblib.load(MODEL_FILE)
    print("✅ Hackathon prediction model loaded successfully.")
except FileNotFoundError:
    print(f"❌ ERROR: Model file not found at '{MODEL_FILE}'. Please run train_hackathon_model.py first.")
    model_pipeline = None

def predict_yield(input_data: dict):
    """
    Predicts crop yield using the trained hackathon model.
    """
    if model_pipeline is None:
        return {"error": "Model not loaded. Please train the model first."}

    try:
        # Convert the input dictionary from the API into a pandas DataFrame
        input_df = pd.DataFrame([input_data])

        # Use the pipeline to preprocess the input and make a prediction
        prediction = model_pipeline.predict(input_df)

        # The result is a numpy array, so we get the first (and only) element
        predicted_yield = prediction[0]

        return {
            "predicted_yield_tons_per_hectare": round(float(predicted_yield), 2),
            "input_features": input_data
        }

    except Exception as e:
        return {"error": f"Prediction error: {str(e)}"}

