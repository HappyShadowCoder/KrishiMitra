from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware  # <-- IMPORT THE CORS MIDDLEWARE
import os

# Import your custom logic
from predict_hackathon import predict_yield
from query_engine import run_query_engine
from data_fetcher import fetch_weather_by_town, fetch_weather_forecast_by_town

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="KrishiMitra AI Backend")

# --- ENABLE CORS ---
# This is the crucial part that allows your frontend to communicate with this backend.
origins = ["*"]  # Allow all origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

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

# 4. Health Check
@app.get("/ping")
def ping():
    return {"status": "ok"}

