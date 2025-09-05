import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  CloudRain,
  Thermometer,
  Droplet,
  Bell,
  Wind,
  CalendarDays,
} from "lucide-react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  BarChart,
  Bar,
  AreaChart,
  Area,
  CartesianGrid,
} from "recharts";

export default function Weather({ weather, setAlerts }) {
  const [expanded, setExpanded] = useState(false);

  // Utility: prevents NaN rendering
  const safeNumber = (val, fallback = 0) =>
    typeof val === "number" && !isNaN(val) ? val : fallback;

  // The formatted data is now passed directly from Home.jsx
  const formattedForecast = weather.forecast;

  return (
    <Card className="overflow-hidden bg-gradient-to-br from-blue-100 via-white to-blue-200 shadow-xl rounded-2xl">
      <motion.div
        className="p-6"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        {/* Header */}
        <div className="flex justify-between items-start">
          <div>
            <h3 className="text-base font-semibold text-gray-700">Weather</h3>
            <div className="mt-3">
              <div className="text-4xl font-extrabold text-gray-900">
                {safeNumber(weather.tempC)}°C
              </div>
              <div className="text-sm text-gray-600">{weather.condition}</div>
              <div className="mt-3 text-sm text-gray-700 flex flex-wrap gap-4 items-center">
                <CloudRain className="w-4 h-4 text-blue-500" />
                {Math.round(safeNumber(weather.rainProbability))}% rain
                <Wind className="w-4 h-4 ml-3 text-gray-600" />
                {Math.round(safeNumber(weather.windSpeed))} km/h wind
                <Droplet className="w-4 h-4 ml-3 text-cyan-600" />
                {safeNumber(weather.humidity)}% humidity
              </div>
            </div>
            <div className="mt-3 text-xs text-gray-500">
              Last updated:{" "}
              {weather.lastUpdated
                ? weather.lastUpdated.toLocaleTimeString()
                : "—"}
            </div>
          </div>

          <div className="flex flex-col gap-3 items-end">
            <div className="rounded-full bg-white p-2 shadow-md">
              <Thermometer className="w-6 h-6 text-red-500" />
            </div>
            {/* The alert button has been removed as requested. */}
          </div>
        </div>

        {/* Toggle Button for < xl screens */}
        <div className="mt-4">
          <button
            onClick={() => setExpanded(!expanded)}
            className="w-full text-center py-2 text-sm font-semibold text-blue-600 border rounded-lg hover:bg-blue-50"
          >
            {expanded ? "Hide 5-Day Forecast" : "Show 5-Day Forecast"}
          </button>
        </div>

        {/* Charts */}
        {expanded && formattedForecast.length > 0 && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.4 }}
            className="mt-6 grid grid-cols-1 gap-6"
          >
            <h4 className="text-lg font-semibold text-gray-800 flex items-center">
              <CalendarDays className="w-5 h-5 mr-2 text-green-600" /> 5-Day
              Forecast
            </h4>

            {/* Temperature Trend (Line Chart) */}
            <div className="bg-white p-4 rounded-lg shadow-sm">
              <h5 className="text-md font-medium text-gray-700 mb-2">
                Temperature Trend (°C)
              </h5>
              <ResponsiveContainer width="100%" height={200}>
                <LineChart
                  data={formattedForecast}
                  margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                  <XAxis dataKey="time" stroke="#666" fontSize={12} />
                  <YAxis
                    stroke="#666"
                    fontSize={12}
                    domain={["auto", "auto"]}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#fff",
                      border: "1px solid #ccc",
                      borderRadius: "8px",
                    }}
                  />
                  <Line
                    type="monotone"
                    dataKey="temp"
                    stroke="#ef4444"
                    strokeWidth={2}
                    dot={{ r: 3 }}
                    activeDot={{ r: 5 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Rain Probability (Bar Chart) */}
            <div className="bg-white p-4 rounded-lg shadow-sm">
              <h5 className="text-md font-medium text-gray-700 mb-2">
                Rain Probability (%)
              </h5>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart
                  data={formattedForecast}
                  margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                  <XAxis dataKey="time" stroke="#666" fontSize={12} />
                  <YAxis stroke="#666" fontSize={12} domain={[0, 100]} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#fff",
                      border: "1px solid #ccc",
                      borderRadius: "8px",
                    }}
                  />
                  <Bar
                    dataKey="rainProbability"
                    fill="#3b82f6"
                    radius={[4, 4, 0, 0]}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Wind Speed (Area Chart) */}
            <div className="bg-white p-4 rounded-lg shadow-sm">
              <h5 className="text-md font-medium text-gray-700 mb-2">
                Wind Speed (km/h)
              </h5>
              <ResponsiveContainer width="100%" height={200}>
                <AreaChart
                  data={formattedForecast}
                  margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
                >
                  <defs>
                    <linearGradient
                      id="windGradient"
                      x1="0"
                      y1="0"
                      x2="0"
                      y2="1"
                    >
                      <stop offset="0%" stopColor="#0ea5e9" stopOpacity={0.8} />
                      <stop
                        offset="100%"
                        stopColor="#38bdf8"
                        stopOpacity={0.1}
                      />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                  <XAxis dataKey="time" stroke="#666" fontSize={12} />
                  <YAxis
                    stroke="#666"
                    fontSize={12}
                    domain={["auto", "auto"]}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#fff",
                      border: "1px solid #ccc",
                      borderRadius: "8px",
                    }}
                  />
                  <Area
                    type="monotone"
                    dataKey="windSpeed"
                    stroke="#0284c7"
                    strokeWidth={2}
                    fill="url(#windGradient)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </motion.div>
        )}
      </motion.div>
    </Card>
  );
}

function Card({ children, className = "" }) {
  return (
    <div className={`rounded-lg bg-white p-4 shadow ${className}`}>
      {children}
    </div>
  );
}
