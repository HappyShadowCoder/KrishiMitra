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
import { useNavigate } from "react-router-dom";
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
  const navigate = useNavigate();
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
    <div className="relative w-screen h-screen overflow-hidden flex flex-col items-center justify-between">
      {/* Background with moving crops */}
      <div className="absolute inset-0 z-0">
        <style>
          {`
            @keyframes slide {
              0% { transform: translateX(0); }
              100% { transform: translateX(-50%); }
            }
            .crop-slider {
              animation: slide 20s linear infinite;
              white-space: nowrap;
              position: absolute;
              top: 0;
              left: 0;
              width: 200%;
              height: 100%;
              display: flex;
              align-items: center;
            }
            .crop-slider img {
              width: auto;
              height: 100%;
              margin-right: 20px;
              object-fit: cover;
            }
          `}
        </style>
        <div className="crop-slider opacity-20">
          <img src="https://wallpaperaccess.com/full/3830895.jpg" alt="Wheat" />
          <img
            src="https://www.apnikheti.com/upload/crops/5431idea99rice1.JPG"
            alt="Rice"
          />
          <img
            src="https://tse2.mm.bing.net/th/id/OIP.vprCAmXPbFAgOMo8MQIXGAHaE8?rs=1&pid=ImgDetMain&o=7&rm=3"
            alt="Corn"
          />
          <img src="" alt="Sugarcane" />
          <img
            src="https://media.istockphoto.com/photos/cotton-crop-picture-id1060253414?k=20&m=1060253414&s=170667a&w=0&h=xgZ9_ufW5hkMVbAKhVd0qHwCemwfC6ORWAN6Lfr-LD4="
            alt="Cotton"
          />
        </div>
      </div>

      <div className="z-10 flex flex-col justify-center items-center h-full">
        <motion.div
          className="text-center mb-5 mt-20"
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-4xl md:text-5xl font-bold text-green-700 mb-4">
            Smart Farming Dashboard
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Real-time insights into soil, weather, and crop growth for better
            farming decisions.
          </p>
        </motion.div>
        <div className="flex gap-5 mt-8">
          <button
            className="px-4 py-2 bg-black/80 text-white rounded-xl font-semibold tracking-wide hover:bg-black/90 hover:scale-110 transition-all duration-300 ease-in-out"
            onClick={() => navigate("/home")}
          >
            Login
          </button>
          <button
            className="px-4 py-2 bg-green-800/90 text-white rounded-xl font-semibold tracking-wide hover:bg-green-800 hover:scale-110 transition-all duration-300 ease-in-out"
            onClick={() => navigate("/home")}
          >
            Explore
          </button>
        </div>
      </div>

      <div className="z-10 flex flex-col items-center p-8 bg-white/70 backdrop-blur-sm w-full">
        <div className="overflow-hidden whitespace-nowrap w-full mt-4">
          <div className="marquee inline-block text-black/60 text-lg">
            <span className="mx-16 font-bold">
              🚀 Soil Testing and Health Analysis
            </span>
            <span className="mx-16 font-bold">
              🔥 Real Time Updates and Threat Detection
            </span>
            <span className="mx-16 font-bold">
              💻 Always Adapting • Easy To Use • Mobile Friendly
            </span>
            <span className="mx-16 font-bold">🚀 Voice Activated Response</span>
            <span className="mx-16 font-bold">🔥 Zero Payment Required</span>
          </div>
        </div>
      </div>
    </div>
  );
}
