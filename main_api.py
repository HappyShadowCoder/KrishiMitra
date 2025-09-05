from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# --- Import your custom modules ---
from predict_hackathon import predict_yield
from data_fetcher import fetch_weather_by_town
from query_engine import run_query_engine # <--- IMPORT THE AI LOGIC

app = FastAPI(title="KrishiMitra AI Backend")

# --- State to Region Mapping ---
STATE_TO_REGION = {
    # North India
    "jammu and kashmir": "North", "himachal pradesh": "North", "punjab": "North",
    "chandigarh": "North", "uttarakhand": "North", "haryana": "North",
    "delhi": "North", "uttar pradesh": "North", "ladakh": "North",

    # East India (including Northeast)
    "bihar": "East", "jharkhand": "East", "odisha": "East", "west bengal": "East",
    "arunachal pradesh": "East", "assam": "East", "manipur": "East",
    "meghalaya": "East", "mizoram": "East", "nagaland": "East",
    "sikkim": "East", "tripura": "East",

    # South India
    "andhra pradesh": "South", "telangana": "South", "karnataka": "South",
    "kerala": "South", "tamil nadu": "South", "puducherry": "South",
    "andaman and nicobar islands": "South", "lakshadweep": "South",

    # West India
    "rajasthan": "West", "gujarat": "West", "goa": "West", "maharashtra": "West",
    "dadra and nagar haveli and daman and diu": "West", "madhya pradesh": "West",
    "chhattisgarh": "West"
}

def get_region_from_state(state_name: str):
    clean_state = state_name.strip().lower()
    return STATE_TO_REGION.get(clean_state)

# --- NEW: Q&A Bot Endpoint ---
class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
def ask(req: QueryRequest):
    """
    Handles questions for the AI Q&A engine.
    """
    answer = run_query_engine(req.question)
    return {"answer": answer}

# --- Yield Predictor Endpoint ---
class PredictWithLiveRainfallRequest(BaseModel):
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
def predict(req: PredictWithLiveRainfallRequest):
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

# --- Weather Dashboard Endpoint ---
class TownRequest(BaseModel):
    town: str

@app.post("/weather")
def weather(req: TownRequest):
    data = fetch_weather_by_town(req.town)
    return {"weather_data": data}

# --- Health Check ---
@app.get("/ping")
def ping():
    return {"status": "ok"}

