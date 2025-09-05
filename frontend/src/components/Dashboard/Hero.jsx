import { motion, AnimatePresence } from "framer-motion";
import { useState } from "react";
// import CountUp from "react-countup"; // Temporarily disabled to fix build error
import {
  CloudRain,
  Droplet,
  Thermometer,
  Leaf,
  Sun,
  BarChart3,
} from "lucide-react";
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function Hero() {
  const [view, setView] = useState("weather");

  const weatherMetrics = [
    {
      title: "Rainfall Prediction",
      value: 78,
      icon: CloudRain,
      color: "text-blue-600",
    },
    {
      title: "Precipitation Chance",
      value: 65,
      icon: Droplet,
      color: "text-green-600",
    },
    {
      title: "Soil Moisture",
      value: 42,
      icon: Thermometer,
      color: "text-yellow-600",
    },
  ];

  const soilMetrics = [
    { title: "Soil Type", value: "Loamy", icon: Leaf, color: "text-green-700" },
    {
      title: "Soil Health",
      value: "Good",
      icon: BarChart3,
      color: "text-blue-700",
    },
    {
      title: "Soil pH",
      value: 6.5,
      icon: Thermometer,
      color: "text-purple-600",
    },
    { title: "Organic Matter", value: 45, icon: Sun, color: "text-orange-600" },
  ];

  const soilData = [
    { name: "Organic Matter", value: 45, color: "#f97316" },
    { name: "Minerals", value: 40, color: "#a855f7" },
    { name: "Water", value: 10, color: "#3b82f6" },
    { name: "Air", value: 5, color: "#eab308" },
  ];

  const cropData = [
    { name: "Jan", growth: 10 },
    { name: "Feb", growth: 25 },
    { name: "Mar", growth: 50 },
    { name: "Apr", growth: 80 },
    { name: "May", growth: 60 },
    { name: "Jun", growth: 90 },
  ];

  return (
    <div className="bg-gray-50 min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-5xl font-bold text-center text-gray-800 mb-4">
          Welcome to <span className="text-green-600">KrishiMitra</span>
        </h1>
        <p className="text-lg text-center text-gray-600 mb-12">
          Your AI-powered assistant for modern farming.
        </p>

        {/* Metrics Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
          {weatherMetrics.map((metric, i) => (
            <motion.div
              key={i}
              className="bg-white shadow-lg rounded-2xl p-6 flex items-center space-x-6"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
            >
              <div
                className={`p-4 rounded-full bg-opacity-10 ${metric.color.replace(
                  "text-",
                  "bg-"
                )}`}
              >
                <metric.icon className={`w-8 h-8 ${metric.color}`} />
              </div>
              <div>
                <p className="text-gray-500">{metric.title}</p>
                <p className="text-3xl font-bold text-gray-800">
                  {/* <CountUp end={metric.value} duration={2} />% */}
                  {metric.value}%
                </p>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Soil Composition */}
          <motion.div
            className="bg-white shadow-lg rounded-2xl p-6"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h3 className="text-xl font-semibold text-gray-800 mb-4">
              Soil Composition
            </h3>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={soilData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  fill="#8884d8"
                  paddingAngle={5}
                  dataKey="value"
                >
                  {soilData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: "white",
                    borderRadius: "8px",
                    border: "1px solid #e5e7eb",
                  }}
                />
              </PieChart>
            </ResponsiveContainer>

            {/* Custom Legend */}
            <div className="flex justify-center mt-4 gap-6">
              {soilData.map((entry, i) => (
                <div key={i} className="flex items-center space-x-2">
                  <div
                    className="w-4 h-4 rounded-full"
                    style={{ backgroundColor: entry.color }}
                  ></div>
                  <p className="text-sm font-medium text-gray-700">
                    {entry.name}
                  </p>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Crop Growth */}
          <motion.div
            className="bg-green-50 shadow-md rounded-2xl p-6"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <h3 className="text-xl font-semibold text-gray-800 mb-4">
              Crop Growth Over Months
            </h3>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={cropData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="growth" fill="#16a34a" />
              </BarChart>
            </ResponsiveContainer>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
