import React, { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Bot, Leaf, Loader2, MapPin, ArrowLeft, Tractor } from "lucide-react";
import Weather from "./Weather.jsx";
import { useNavigate } from "react-router-dom";

// --- Configuration ---
const API_URL = "http://127.0.0.1:8000"; // Your FastAPI backend URL

// --- List of Indian States for Dropdown ---
const STATES_LIST = [
  "Andhra Pradesh",
  "Arunachal Pradesh",
  "Assam",
  "Bihar",
  "Chhattisgarh",
  "Goa",
  "Gujarat",
  "Haryana",
  "Himachal Pradesh",
  "Jharkhand",
  "Karnataka",
  "Kerala",
  "Madhya Pradesh",
  "Maharashtra",
  "Manipur",
  "Meghalaya",
  "Mizoram",
  "Nagaland",
  "Odisha",
  "Punjab",
  "Rajasthan",
  "Sikkim",
  "Tamil Nadu",
  "Telangana",
  "Tripura",
  "Uttar Pradesh",
  "Uttarakhand",
  "West Bengal",
  "Andaman and Nicobar Islands",
  "Chandigarh",
  "Dadra and Nagar Haveli and Daman and Diu",
  "Delhi",
  "Jammu and Kashmir",
  "Ladakh",
  "Lakshadweep",
  "Puducherry",
];

// --- Location Modal Component ---
const LocationModal = ({ isOpen, onSave }) => {
  const [town, setTown] = useState("");
  const [state, setState] = useState("");

  const handleSave = () => {
    if (town.trim() && state.trim()) {
      onSave({ town, state });
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-2xl p-8 shadow-2xl w-full max-w-sm">
        <h2 className="text-2xl font-bold mb-4 flex items-center text-gray-800">
          <MapPin className="mr-2 text-green-600" /> Set Your Location
        </h2>
        <p className="text-gray-600 mb-6">
          Please provide your location for accurate weather and predictions.
        </p>
        <div className="space-y-4">
          <input
            type="text"
            value={town}
            onChange={(e) => setTown(e.target.value)}
            placeholder="Enter Town Name (e.g., Jaipur)"
            className="w-full bg-gray-100 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-green-500 text-gray-800"
          />
          {/* State Dropdown */}
          <select
            value={state}
            onChange={(e) => setState(e.target.value)}
            className="w-full bg-gray-100 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-green-500 text-gray-800"
          >
            <option value="" disabled>
              Select a State
            </option>
            {STATES_LIST.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
        </div>
        <button
          onClick={handleSave}
          disabled={!town.trim() || !state.trim()}
          className="w-full bg-green-600 hover:bg-green-700 text-white p-3 mt-6 rounded-lg font-bold text-lg disabled:bg-gray-400"
        >
          Save & Continue
        </button>
      </div>
    </div>
  );
};

// --- New Prediction Form Modal Component ---
const PredictionFormModal = ({
  isOpen,
  onSave,
  location,
  currentTemp,
  weatherCondition,
}) => {
  const [formData, setFormData] = useState({
    Soil_Type: "",
    Crop: "",
    Fertilizer_Used: false,
    Irrigation_Used: false,
    Days_to_Harvest: "",
  });

  useEffect(() => {
    // Reset form data when modal opens
    setFormData({
      Soil_Type: "",
      Crop: "",
      Fertilizer_Used: false,
      Irrigation_Used: false,
      Days_to_Harvest: "",
    });
  }, [isOpen]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSave = () => {
    const fullData = {
      ...formData,
      State: location.state,
      Town: location.town,
      Temperature_Celsius: parseFloat(currentTemp),
      Weather_Condition: weatherCondition,
      Days_to_Harvest: parseInt(formData.Days_to_Harvest, 10),
    };
    onSave(fullData);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <motion.div
        className="bg-white rounded-2xl p-8 shadow-2xl w-full max-w-lg"
        initial={{ y: -50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        exit={{ y: 50, opacity: 0 }}
        transition={{ type: "spring", stiffness: 100 }}
      >
        <h2 className="text-2xl font-bold mb-4 flex items-center text-gray-800">
          <Leaf className="mr-2 text-green-600" /> Yield Prediction Details
        </h2>
        <p className="text-gray-600 mb-6">
          Please provide some details for an accurate crop yield prediction.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Soil Type
            </label>
            <input
              type="text"
              name="Soil_Type"
              value={formData.Soil_Type}
              onChange={handleChange}
              placeholder="e.g., Loam, Clay"
              className="w-full bg-gray-100 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-green-500 mt-1 text-gray-800"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Crop
            </label>
            <input
              type="text"
              name="Crop"
              value={formData.Crop}
              onChange={handleChange}
              placeholder="e.g., Wheat, Rice"
              className="w-full bg-gray-100 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-green-500 mt-1 text-gray-800"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Days to Harvest
            </label>
            <input
              type="number"
              name="Days_to_Harvest"
              value={formData.Days_to_Harvest}
              onChange={handleChange}
              placeholder="e.g., 120"
              className="w-full bg-gray-100 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-green-500 mt-1 text-gray-800"
            />
          </div>
          <div className="flex items-center space-x-4 pt-6">
            <div className="flex items-center">
              <input
                type="checkbox"
                name="Fertilizer_Used"
                checked={formData.Fertilizer_Used}
                onChange={handleChange}
                className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
              />
              <label
                htmlFor="Fertilizer_Used"
                className="ml-2 block text-sm text-gray-900"
              >
                Fertilizer Used
              </label>
            </div>
            <div className="flex items-center">
              <input
                type="checkbox"
                name="Irrigation_Used"
                checked={formData.Irrigation_Used}
                onChange={handleChange}
                className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
              />
              <label
                htmlFor="Irrigation_Used"
                className="ml-2 block text-sm text-gray-900"
              >
                Irrigation Used
              </label>
            </div>
          </div>
        </div>
        <button
          onClick={handleSave}
          disabled={
            !formData.Soil_Type || !formData.Crop || !formData.Days_to_Harvest
          }
          className="w-full bg-green-600 hover:bg-green-700 text-white p-3 mt-6 rounded-lg font-bold text-lg disabled:bg-gray-400"
        >
          Get Prediction
        </button>
      </motion.div>
    </div>
  );
};

export default function Home() {
  const navigate = useNavigate();
  // --- State Management ---
  const [isLocationModalOpen, setIsLocationModalOpen] = useState(true);
  const [isPredictionFormOpen, setIsPredictionFormOpen] = useState(false);
  const [weatherData, setWeatherData] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [aiAnswer, setAiAnswer] = useState(
    "Ask me a question about agriculture!"
  );
  const [isLoading, setIsLoading] = useState({
    weather: false,
    prediction: false,
    ask: false,
  });
  const [userInput, setUserInput] = useState({
    town: "",
    state: "",
    question: "How to improve soil health?",
  });
  const isMounted = useRef(true);

  // --- API Fetching Logic ---
  const fetchWeatherData = async (town) => {
    if (!town) return;
    setIsLoading((prev) => ({ ...prev, weather: true }));
    try {
      const response = await fetch(`${API_URL}/weather`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ town }),
      });
      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "Weather data could not be fetched.");
      }
      const data = await response.json();

      // Transform the data to the format expected by Weather.jsx
      const transformedWeather = {
        tempC: data.current.current_conditions.temperature_celsius,
        condition: data.current.current_conditions.description,
        rainProbability: data.forecast.forecast[0].rain_chance_percent,
        windSpeed: data.current.current_conditions.wind_speed_mps,
        humidity: data.current.current_conditions.humidity_percent,
        lastUpdated: new Date(),
        forecast: data.forecast.forecast.map((entry) => ({
          time: new Date(entry.datetime).toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
          temp: entry.temperature_celsius,
          rainProbability: entry.rain_chance_percent,
          windSpeed: entry.wind_speed_mps,
        })),
      };

      if (isMounted.current) setWeatherData(transformedWeather);
    } catch (error) {
      console.error("Error fetching weather:", error);
      if (isMounted.current) setWeatherData({ error: error.message });
    } finally {
      if (isMounted.current)
        setIsLoading((prev) => ({ ...prev, weather: false }));
    }
  };

  const fetchPrediction = async (predictionInput) => {
    setIsLoading((prev) => ({ ...prev, prediction: true }));
    setIsPredictionFormOpen(false); // Close the form modal

    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(predictionInput),
      });
      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "Prediction request failed.");
      }
      const data = await response.json();
      if (isMounted.current) setPrediction(data);
    } catch (error) {
      console.error("Error fetching prediction:", error);
      if (isMounted.current) setPrediction({ error: error.message });
    } finally {
      if (isMounted.current)
        setIsLoading((prev) => ({ ...prev, prediction: false }));
    }
  };

  const askAi = async () => {
    if (!userInput.question.trim()) return;
    setIsLoading((prev) => ({ ...prev, ask: true }));
    setAiAnswer("Thinking...");
    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userInput.question }),
      });
      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "AI assistant is currently offline.");
      }
      const data = await response.json();
      if (isMounted.current) setAiAnswer(data.answer);
    } catch (error) {
      console.error("Error asking AI:", error);
      if (isMounted.current) setAiAnswer(error.message);
    } finally {
      if (isMounted.current) setIsLoading((prev) => ({ ...prev, ask: false }));
    }
  };

  // --- Handlers ---
  const handleLocationSave = (location) => {
    setUserInput((prev) => ({
      ...prev,
      town: location.town,
      state: location.state,
    }));
    fetchWeatherData(location.town);
    setIsLocationModalOpen(false);
  };

  const handlePredictionClick = () => {
    if (!userInput.town) {
      alert("Please set your location first.");
      return;
    }
    if (!weatherData) {
      alert("Please wait for weather data to load.");
      return;
    }
    setIsPredictionFormOpen(true);
  };

  // --- Effects ---
  useEffect(() => {
    // Cleanup function
    return () => {
      isMounted.current = false;
    };
  }, []);

  return (
    <>
      <LocationModal isOpen={isLocationModalOpen} onSave={handleLocationSave} />
      <PredictionFormModal
        isOpen={isPredictionFormOpen}
        onSave={fetchPrediction}
        location={userInput}
        currentTemp={weatherData?.tempC}
        weatherCondition={weatherData?.condition}
      />
      <div className="bg-gray-100 min-h-screen p-4 sm:p-6 font-poppins">
        {/* Dashboard Nav Bar */}
        <nav className="flex items-center justify-between p-4 bg-white rounded-lg shadow mb-6">
          <div className="flex items-center space-x-2">
            <Tractor className="text-green-600 w-7 h-7" />
            <h1 className="text-lg md:text-xl font-bold text-green-700">
              Krishi Mitra
            </h1>
          </div>
          <button
            onClick={() => navigate("/")}
            className="flex items-center gap-2 px-4 py-2 bg-gray-100 rounded-lg text-gray-600 hover:bg-gray-200 transition"
          >
            <ArrowLeft className="w-5 h-5" />
            Go Back
          </button>
        </nav>

        <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1 flex flex-col gap-6">
            {/* Conditional Rendering for Weather Component */}
            {weatherData && !weatherData.error ? (
              <Weather weather={weatherData} isLoading={isLoading.weather} />
            ) : (
              <div className="bg-white p-6 rounded-2xl shadow-lg text-center min-h-[150px] flex items-center justify-center">
                <p className="text-gray-500">
                  {weatherData?.error ||
                    "Please set your location to get weather data."}
                </p>
              </div>
            )}
          </div>

          <div className="lg:col-span-2 flex flex-col gap-6">
            <div className="bg-white p-6 rounded-2xl shadow-lg">
              <h2 className="text-xl font-bold mb-4 flex items-center text-gray-800">
                <Leaf className="mr-2 text-green-600" />
                Yield Prediction
              </h2>
              <p className="text-sm text-gray-500 mb-4">
                Our model is 97% accurate in its predictions.
              </p>
              <div className="bg-gray-50 border-2 border-dashed border-gray-200 p-6 rounded-lg text-center min-h-[150px] flex items-center justify-center">
                {prediction && !prediction.error ? (
                  <div>
                    <p className="text-gray-500">
                      Predicted Yield for {prediction.input_features.Crop}
                    </p>
                    <p className="text-5xl font-bold text-green-600 my-2">
                      {prediction.predicted_yield_tons_per_hectare}
                      <span className="text-2xl font-normal text-gray-500">
                        {" "}
                        tons/ha
                      </span>
                    </p>
                    <p className="text-sm text-gray-400">
                      Calculated using {prediction.live_rainfall_used_mm}mm of
                      live rainfall data.
                    </p>
                  </div>
                ) : (
                  <p className="text-gray-500">
                    {prediction?.error ||
                      "Click the button to generate a yield prediction."}
                  </p>
                )}
              </div>
              <button
                onClick={handlePredictionClick}
                disabled={
                  isLoading.prediction || !userInput.town || !weatherData
                }
                className="w-full bg-green-600 hover:bg-green-700 text-white p-3 mt-4 rounded-lg font-bold text-lg disabled:bg-gray-400 flex items-center justify-center"
              >
                {isLoading.prediction && (
                  <Loader2 className="animate-spin mr-2" />
                )}
                {isLoading.prediction
                  ? "Calculating..."
                  : `Predict Yield in ${userInput.town || "your town"}`}
              </button>
            </div>

            {/* AI Chatbot Section */}
            <div className="bg-white p-6 rounded-2xl shadow-lg">
              <h2 className="text-xl font-bold mb-4 flex items-center text-gray-800">
                <Bot className="mr-2 text-green-600" />
                Ask KrishiMitra AI
              </h2>
              <div className="flex items-center space-x-2 mb-4">
                <input
                  type="text"
                  value={userInput.question}
                  onChange={(e) =>
                    setUserInput((prev) => ({
                      ...prev,
                      question: e.target.value,
                    }))
                  }
                  onKeyDown={(e) => e.key === "Enter" && askAi()}
                  placeholder="e.g., How to control pests?"
                  className="w-full bg-gray-100 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-green-500 text-gray-800"
                />
                <button
                  onClick={askAi}
                  disabled={isLoading.ask}
                  className="bg-green-600 hover:bg-green-700 text-white p-3 rounded-lg disabled:bg-gray-400 flex-shrink-0"
                >
                  {isLoading.ask ? <Loader2 className="animate-spin" /> : "Ask"}
                </button>
              </div>
              <div className="bg-gray-100 p-4 rounded-lg min-h-[120px] text-gray-700">
                {aiAnswer}
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
