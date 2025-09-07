import { motion } from "framer-motion";
import {
  Mail,
  Phone,
  MapPin,
  Facebook,
  Twitter,
  Instagram,
  Linkedin,
  ArrowLeft,
  Tractor,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function Contact() {
  const navigate = useNavigate();
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
      <div className="py-20 px-6 md:px-16 lg:px-24 bg-gradient-to-br from-green-50 via-white to-green-100">
        {/* Header */}
        <motion.div
          className="text-center mb-12"
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-4xl md:text-5xl font-bold text-green-700 mb-4">
            Contact Us
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Have questions, feedback, or partnership ideas? Let’s connect and
            grow together.
          </p>
        </motion.div>

        {/* Contact + Form */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
          {/* Info Cards */}
          <motion.div
            className="flex flex-col justify-center space-y-6"
            initial={{ opacity: 0, x: -40 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.7 }}
          >
            <div className="flex items-center space-x-4 bg-green-50 p-4 rounded-xl shadow hover:shadow-lg transition">
              <Mail className="text-green-600 w-7 h-7" />
              <span className="text-gray-700">krishimitra@example.com</span>
            </div>

            <div className="flex items-center space-x-4 bg-green-50 p-4 rounded-xl shadow hover:shadow-lg transition">
              <Phone className="text-green-600 w-7 h-7" />
              <span className="text-gray-700">+91 98765 43210</span>
            </div>

            <div className="flex items-center space-x-4 bg-green-50 p-4 rounded-xl shadow hover:shadow-lg transition">
              <MapPin className="text-green-600 w-7 h-7" />
              <span className="text-gray-700">Jaipur, India</span>
            </div>

            {/* Social Links */}
            <div className="flex space-x-5 mt-6">
              {[
                { icon: Facebook, color: "hover:text-blue-600" },
                { icon: Twitter, color: "hover:text-sky-500" },
                { icon: Instagram, color: "hover:text-pink-500" },
                { icon: Linkedin, color: "hover:text-blue-700" },
              ].map((s, i) => (
                <motion.a
                  key={i}
                  href="#"
                  className={`text-gray-600 transition ${s.color}`}
                  whileHover={{ scale: 1.2, rotate: 5 }}
                  whileTap={{ scale: 0.9 }}
                >
                  <s.icon className="w-7 h-7" />
                </motion.a>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Footer */}
        <motion.div
          className="mt-20 text-center text-gray-500 text-sm"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
        >
          <p>© {new Date().getFullYear()} Krishi Mitra. All Rights Reserved.</p>
          <p className="mt-1">Created by Krishi Mitra Team 🌱</p>
        </motion.div>
      </div>
    </section>
  );
}
