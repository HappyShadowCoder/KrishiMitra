import pandas as pd
import requests
import time
from tqdm import tqdm
import os

# --- Configuration ---
INPUT_CSV = "crop-wise-area-production-yield.csv"
# MODIFIED: Pointing to your new coordinates file
COORDS_CSV = "UnApportionedIdentifiers.csv"
OUTPUT_CSV = "enriched_crop_yield_data.csv"
CHECKPOINT_FILE = "checkpoint.csv"

# --- Mappings and Constants ---
# Define date ranges for Indian agricultural seasons
SEASON_MAP = {
    "Kharif": ("06-01", "10-31"),
    "Rabi": ("11-01", "03-31"),
    "Summer": ("03-01", "06-30"),
    "Whole Year": ("01-01", "12-31"),
    "Autumn": ("09-01", "12-31"),
    "Winter": ("12-01", "02-28")
}


# --- API Helper Functions ---

def fetch_soil_for_model(lat, lon, cache):
    """Fetches soil data from SoilGrids, using a cache to avoid redundant calls."""
    cache_key = f"{lat:.2f},{lon:.2f}"
    if cache_key in cache:
        return cache[cache_key]

    url = (
        f"https://rest.isric.org/soilgrids/v2.0/properties/query"
        f"?lon={lon}&lat={lat}"
        f"&property=phh2o&property=nitrogen&property=phosphorus&property=potassium"
        f"&depth=0-5cm&value=mean"
    )
    try:
        resp = requests.get(url, timeout=20).json()
        if "properties" not in resp:
            return None

        props = resp["properties"]["layers"]

        def extract_value(layer, default):
            val = next((v.get("value") for v in layer.get("depths", []) if "value" in v), None)
            # SoilGrids returns values scaled by 10 or 100
            if layer['name'] == 'phh2o' and val is not None: return val / 10.0
            if layer['name'] == 'nitrogen' and val is not None: return val / 100.0
            return val if val is not None else default

        soil_data = {
            "soil_ph": extract_value(next(p for p in props if p['name'] == 'phh2o'), 7.0),
            "soil_nitrogen": extract_value(next(p for p in props if p['name'] == 'nitrogen'), 0.2),
            "soil_phosphorus": extract_value(next(p for p in props if p['name'] == 'phosphorus'), 10.0),
            "soil_potassium": extract_value(next(p for p in props if p['name'] == 'potassium'), 50.0)
        }
        cache[cache_key] = soil_data
        return soil_data
    except requests.RequestException:
        return None


def fetch_nasa_weather(lat, lon, start_date, end_date):
    """Fetches historical weather data from NASA POWER API."""
    base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "parameters": "T2M,PRECTOTCORR,RH2M",
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start_date,
        "end": end_date,
        "format": "JSON"
    }
    try:
        response = requests.get(base_url, params=params, timeout=30)
        if response.status_code != 200:
            return None

        data = response.json()

        temp_data = [v for v in data['properties']['parameter']['T2M'].values() if v != -999]
        precip_data = [v for v in data['properties']['parameter']['PRECTOTCORR'].values() if v != -999]
        humidity_data = [v for v in data['properties']['parameter']['RH2M'].values() if v != -999]

        return {
            "temperature": sum(temp_data) / len(temp_data) if temp_data else None,
            "rainfall": sum(precip_data),
            "humidity": sum(humidity_data) / len(humidity_data) if humidity_data else None,
        }
    except requests.RequestException:
        return None


# --- Main Script ---

def main():
    print("Starting data enrichment process with 'UnApportionedIdentifiers.csv'...")

    # Load input files
    if not os.path.exists(INPUT_CSV):
        print(f"❌ Error: Input file '{INPUT_CSV}' not found.")
        return
    if not os.path.exists(COORDS_CSV):
        print(f"❌ Error: Coordinates file '{COORDS_CSV}' not found.")
        return

    df = pd.read_csv(INPUT_CSV)
    coords_df = pd.read_csv(COORDS_CSV)

    # --- MODIFIED SECTION ---
    # Prepare for processing by renaming columns from your new file
    coords_df = coords_df.rename(columns={
        'District Name': 'district',
        'State Name': 'state',
        'Latitude': 'latitude',
        'Longitude': 'longitude'
    })
    # --- END MODIFIED SECTION ---

    df.columns = df.columns.str.strip().str.lower()
    coords_df['district'] = coords_df['district'].str.strip().str.lower()
    coords_df['state'] = coords_df['state'].str.strip().str.lower()

    coords_map = {
        (row['district'], row['state']): (row['latitude'], row['longitude'])
        for _, row in coords_df.iterrows()
    }

    start_index = 0
    if os.path.exists(CHECKPOINT_FILE):
        print("✅ Checkpoint file found. Resuming process...")
        checkpoint_df = pd.read_csv(CHECKPOINT_FILE)
        start_index = len(checkpoint_df)
        df_to_process = df.iloc[start_index:].copy()
        results = checkpoint_df.to_dict('records')
    else:
        df_to_process = df.copy()
        results = []

    soil_cache = {}

    print(f"Processing {len(df_to_process)} rows, starting from index {start_index}.")

    for index, row in tqdm(df_to_process.iterrows(), total=len(df_to_process), desc="Enriching Data"):
        district = str(row.get('district_name', '')).strip().lower()
        state = str(row.get('state_name', '')).strip().lower()
        year = pd.to_numeric(row.get('year'), errors='coerce')
        season = row.get('season', '').strip()

        coords = coords_map.get((district, state))
        if not coords or pd.isna(year):
            continue

        lat, lon = coords
        start_month_day, end_month_day = SEASON_MAP.get(season, (None, None))
        if not start_month_day:
            continue

        start_year, end_year = int(year), int(year)
        if season == "Rabi":
            end_year += 1

        start_date = f"{start_year}{start_month_day.replace('-', '')}"
        end_date = f"{end_year}{end_month_day.replace('-', '')}"

        weather_data = fetch_nasa_weather(lat, lon, start_date, end_date)
        soil_data = fetch_soil_for_model(lat, lon, soil_cache)

        time.sleep(1)

        new_row = row.to_dict()
        if weather_data: new_row.update(weather_data)
        if soil_data: new_row.update(soil_data)
        results.append(new_row)

        if (len(results) % 200 == 0):
            pd.DataFrame(results).to_csv(CHECKPOINT_FILE, index=False)
            tqdm.write(f"💾 Checkpoint saved at row {start_index + len(results)}")

    print("\n✅ Processing complete. Saving final enriched dataset...")
    final_df = pd.DataFrame(results)
    final_df.to_csv(OUTPUT_CSV, index=False)
    print(f"🎉 Success! Enriched data saved to '{OUTPUT_CSV}'")

    if os.path.exists(CHECKPOINT_FILE):
        os.remove(CHECKPOINT_FILE)


if __name__ == "__main__":
    main()
