from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import torch
import torch.nn.functional as F
from torchvision import transforms, models
from PIL import Image
import io

# Import your custom logic
from predict_hackathon import predict_yield
from query_engine import run_query_engine
from data_fetcher import fetch_weather_by_town, fetch_weather_forecast_by_town

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="KrishiMitra AI Backend")

# --- ENABLE CORS ---
origins = ["*"]  # Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Mapping for human-readable disease names ---
DISEASE_SCIENTIFIC_NAMES = {
    "Apple_scab": "Venturia inaequalis",
    "Apple_Black_rot": "Botryosphaeria obtusa",
    "Apple_Cedar_apple_rust": "Gymnosporangium juniperi-virginianae",
    "Cherry_Powdery_mildew": "Podosphaera cerasi",
    "Cherry_healthy": "Prunus avium",
    "Corn_Cercospora_leaf_spot_Gray_leaf_spot": "Cercospora zeae-maydis / Cercospora zeina",
    "Corn_Common_rust": "Puccinia sorghi",
    "Corn_healthy": "Zea mays",
    "Grape_Black_rot": "Guignardia bidwelli",
    "Grape_Leaf_blight_Isariopsis_leaf_spot": "Pseudocercospora vitis",
    "Grape_healthy": "Vitis vinifera",
    "Peach_Bacterial_spot": "Xanthomonas campestris pv. pruni",
    "Peach_healthy": "Prunus persica",
    "Potato___Early_blight": "Alternaria solani",
    "Potato_Late_blight": "Phytophthora infestans",
    "Potato_healthy": "Solanum tuberosum",
    "Strawberry_Leaf_scorch": "Diplocarpon earlianum",
    "Strawberry_healthy": "Fragaria ananassa",
    "Tomato_Bacterial_spot": "Xanthomonas campestris pv. vesicatoria",
    "Tomato_Early_blight": "Alternaria solani",
    "Tomato_Late_blight": "Phytophthora infestans",
    "Tomato_Leaf_Mold": "Cladosporium fulvum",
    "Tomato_Septoria_leaf_spot": "Septoria lycopersici",
    "Tomato_Spider_mites_Two-spotted_spider_mite": "Tetranychus urticae",
    "Tomato_Target_Spot": "Corynespora cassiicola",
    "Tomato_Yellow_Leaf_Curl_Virus": "Tomato yellow leaf curl virus",
    "Pepper__bell___Bacterial_spot": "Tomato mosaic virus",
    "Tomato_healthy": "Solanum lycopersicum",
}

# --- State to Region Mapping ---
STATE_TO_REGION = {
    "jammu and kashmir": "North", "himachal pradesh": "North", "punjab": "North",
    "chandigarh": "North", "uttarakhand": "North", "haryana": "North",
    "delhi": "North", "uttar pradesh": "North", "ladakh": "North",
    "bihar": "East", "jharkhand": "East", "odisha": "East", "west bengal": "East",
    "arunachal pradesh": "East", "assam": "East", "manipur": "East",
    "meghalaya": "East", "mizoram": "East", "nagaland": "East",
    "sikkim": "East", "tripura": "East",
    "andhra pradesh": "South", "telangana": "South", "karnataka": "South",
    "kerala": "South", "tamil nadu": "South", "puducherry": "South",
    "andaman and nicobar islands": "South", "lakshadweep": "South",
    "rajasthan": "West", "gujarat": "West", "goa": "West", "maharashtra": "West",
    "dadra and nagar haveli and daman and diu": "West", "madhya pradesh": "West",
    "chhattisgarh": "West"
}

def get_region_from_state(state_name: str):
    clean_state = state_name.strip().lower()
    return STATE_TO_REGION.get(clean_state)

# --- Load the trained disease detection model ---
# NOTE: This should be done once when the application starts
MODEL_PATH = 'plant_disease_model_fast.pth'
IMAGE_SIZE = 128

disease_model = None
class_names = []
try:
    if os.path.exists(MODEL_PATH):
        checkpoint = torch.load(MODEL_PATH, map_location=torch.device('cpu'))
        class_names = checkpoint.get('class_names', [])
        
        # Initialize the model structure
        model = models.resnet18()
        num_ftrs = model.fc.in_features
        model.fc = torch.nn.Linear(num_ftrs, len(class_names))
        
        # Load the state dictionary
        model.load_state_dict(checkpoint['model_state_dict'])
        model.eval()  # Set the model to evaluation mode
        disease_model = model
        print("✅ Plant disease model loaded successfully.")
    else:
        print(f"❌ Model file not found at '{MODEL_PATH}'. Disease detection will be unavailable.")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    disease_model = None

predict_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
])


# --- Updated predict_disease function ---
def predict_disease(image_bytes):
    if not disease_model:
        return {"error": "Disease model is not loaded."}

    try:
        # Open and transform image
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image_tensor = predict_transform(image).unsqueeze(0)

        with torch.no_grad():
            outputs = disease_model(image_tensor)
            probabilities = F.softmax(outputs, dim=1)  # use softmax for true confidence
            confidence, predicted_index = torch.max(probabilities, 1)

        predicted_index = predicted_index.item()
        predicted_folder_name = class_names[predicted_index]

        # Map to scientific name
        predicted_scientific_name = DISEASE_SCIENTIFIC_NAMES.get(
            predicted_folder_name, predicted_folder_name
        )

        
        predicted_common_name = predicted_folder_name.replace("_", " ")

        return {
            "predicted_class_index": predicted_index,
            "disease_name_common": predicted_common_name,
            "disease_name_scientific": predicted_scientific_name,
            "confidence": f"{confidence.item() * 100:.2f}%",
        }

    except Exception as e:
        print(f"[Prediction Error] {e}")
        return {"error": "Could not process image or make prediction."}

# --- API Endpoints ---

# 1. Yield Predictor
class PredictRequest(BaseModel):
    State: str
    Town: str
    Soil_Type: str
    Crop: str
    Temperature_Celsius: float
    Fertilizer_Used: bool
    Irrigation_Used: bool
    Weather_Condition: str
    Days_to_Harvest: int

@app.post("/predict")
def predict(req: PredictRequest):
    try:
        weather_data = fetch_weather_by_town(req.Town)
        live_rainfall = weather_data.get("current_conditions", {}).get("rainfall_last_hour_mm", 0.0)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Could not fetch weather for town '{req.Town}'. Error: {e}")

    region = get_region_from_state(req.State)
    if not region:
        raise HTTPException(status_code=400, detail=f"State '{req.State}' not found.")

    model_input_data = req.dict()
    model_input_data['Region'] = region
    model_input_data['Rainfall_mm'] = live_rainfall
    del model_input_data['State']
    del model_input_data['Town']

    result = predict_yield(model_input_data)
    result['live_rainfall_used_mm'] = live_rainfall
    return result

# 2. AI Q&A Bot
class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
def ask(req: QueryRequest):
    answer = run_query_engine(req.question)
    return {"answer": answer}

# 3. Weather Dashboard
class TownRequest(BaseModel):
    town: str

@app.post("/weather")
def weather(req: TownRequest):
    try:
        current = fetch_weather_by_town(req.town)
        forecast = fetch_weather_forecast_by_town(req.town)
        return {"current": current, "forecast": forecast}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# 4. Plant Disease Detector
@app.post("/detect-disease")
async def detect_disease(file: UploadFile = File(...)):
    if not disease_model:
        raise HTTPException(status_code=503, detail="The disease detection model is not available.")
    
    # Read the uploaded file
    image_bytes = await file.read()
    
    # Run the prediction
    prediction_result = predict_disease(image_bytes)
    
    if "error" in prediction_result:
        raise HTTPException(status_code=500, detail=prediction_result["error"])
        
    return prediction_result

# 5. Health Check
@app.get("/ping")
def ping():
    return {"status": "ok"}