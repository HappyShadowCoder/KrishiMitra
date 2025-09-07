import { motion } from "framer-motion";
import { CloudRain, Leaf, TrendingUp, ArrowLeft, Tractor } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function Services() {
  const navigate = useNavigate();
  const services = [
    {
      icon: CloudRain,
      title: "Real-time Weather Forecasts",
      description:
        "Get instant, hyper-local weather updates and 5-day forecasts to plan your farming activities with confidence. Our AI analyzes patterns to predict rain, temperature, and wind speed.",
      color: "bg-blue-100 text-blue-700",
    },
    {
      icon: TrendingUp,
      title: "AI-Powered Yield Prediction",
      description:
        "Input your crop, soil type, and other key variables to receive an accurate yield prediction. Our model, with 97% accuracy, helps you make data-driven decisions for a successful harvest.",
      color: "bg-green-100 text-green-700",
    },
    {
      icon: Leaf,
      title: "Expert Agricultural Advice",
      description:
        "Tap into our extensive knowledge base to get answers to your farming questions. Our chatbot provides reliable advice on pest control, soil health, and best practices.",
      color: "bg-yellow-100 text-yellow-700",
    },
  ];

  return (
    <section className="w-full bg-white font-poppins">
      <nav className="flex items-center justify-between p-4 bg-white rounded-lg shadow mb-6">
        <div className="flex items-center space-x-2">
          <Tractor className="text-green-600 w-7 h-7" />
          <h1 className="text-lg md:text-xl font-bold text-green-700">
            Krishi Mitra
          </h1>
        </div>
        <div className="flex gap-4">
          <button
            onClick={() => navigate("/")}
            className="flex items-center gap-2 px-4 py-2 bg-gray-100 rounded-lg text-gray-600 hover:bg-gray-200 transition"
          >
            <ArrowLeft className="w-5 h-5" />
            Go Back
          </button>
          <button
            onClick={() => navigate("/home")}
            className="flex items-center gap-2 px-4 py-2 bg-green-600 rounded-lg text-white hover:bg-green-700 transition"
          >
            Dashboard
          </button>
        </div>
      </nav>
      <div className="max-w-7xl mx-auto text-center py-20 px-6 md:px-16 lg:px-24">
        <motion.div
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-4xl md:text-5xl font-bold text-green-700 mb-4">
            Our Core Services
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto mb-16">
            Everything you need to make smarter, more sustainable farming
            decisions, powered by AI.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {services.map((service, index) => (
            <motion.div
              key={index}
              className="p-8 rounded-2xl shadow-lg bg-gray-50 flex flex-col items-center text-center transition-transform duration-300 hover:scale-105"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
            >
              <div className={`p-4 rounded-full ${service.color} mb-6`}>
                <service.icon className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">
                {service.title}
              </h3>
              <p className="text-gray-600 leading-relaxed">
                {service.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
