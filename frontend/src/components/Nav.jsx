import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Menu, X, Tractor } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function Nav() {
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();

  return (
    <nav className="absolute top-0 left-0 bg-green-600 fixed w-full overflow-x-hidden z-50 font-poppins">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Left Section: Logo & Name */}
          <motion.div
            className="flex items-center space-x-2 cursor-pointer"
            initial={{ x: -50, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: 0.5 }}
            onClick={() => navigate("/")}
          >
            <Tractor className="text-white w-7 h-7" />
            <h1 className="text-lg md:text-lg whitespace-nowrap font-bold text-white tracking-wide">
              Krishi Mitra
            </h1>
          </motion.div>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center space-x-6">
            <motion.a
              onClick={() => navigate("/")}
              whileHover={{ scale: 1.1, color: "#fef08a" }}
              whileTap={{ scale: 0.95 }}
              transition={{ type: "spring", stiffness: 300 }}
              className="text-white font-medium text-lg hover:text-yellow-200 transition cursor-pointer"
            >
              Home
            </motion.a>
            <motion.a
              onClick={() => navigate("/about")}
              whileHover={{ scale: 1.1, color: "#fef08a" }}
              whileTap={{ scale: 0.95 }}
              transition={{ type: "spring", stiffness: 300 }}
              className="text-white font-medium text-lg hover:text-yellow-200 transition cursor-pointer"
            >
              About
            </motion.a>
            <motion.a
              onClick={() => navigate("/services")}
              whileHover={{ scale: 1.1, color: "#fef08a" }}
              whileTap={{ scale: 0.95 }}
              transition={{ type: "spring", stiffness: 300 }}
              className="text-white font-medium text-lg hover:text-yellow-200 transition cursor-pointer"
            >
              Services
            </motion.a>
            <motion.a
              onClick={() => navigate("/contact")}
              whileHover={{ scale: 1.1, color: "#fef08a" }}
              whileTap={{ scale: 0.95 }}
              transition={{ type: "spring", stiffness: 300 }}
              className="text-white font-medium text-lg hover:text-yellow-200 transition cursor-pointer"
            >
              Contact
            </motion.a>
          </div>

          {/* Mobile Menu Button */}
          <div className="flex md:hidden items-center">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-white focus:outline-none"
            >
              {isOpen ? (
                <X className="w-7 h-7" />
              ) : (
                <Menu className="w-7 h-7" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Dropdown */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.4 }}
            className="md:hidden bg-green-700 shadow-lg"
          >
            <div className="px-4 pt-2 pb-4 space-y-3">
              <motion.a
                onClick={() => {
                  navigate("/");
                  setIsOpen(false);
                }}
                initial={{ x: -20, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 0 * 0.1 }}
                className="block text-white text-lg font-medium hover:text-yellow-200 transition cursor-pointer"
              >
                Home
              </motion.a>
              <motion.a
                onClick={() => {
                  navigate("/about");
                  setIsOpen(false);
                }}
                initial={{ x: -20, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 1 * 0.1 }}
                className="block text-white text-lg font-medium hover:text-yellow-200 transition cursor-pointer"
              >
                About
              </motion.a>
              <motion.a
                onClick={() => {
                  navigate("/services");
                  setIsOpen(false);
                }}
                initial={{ x: -20, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 2 * 0.1 }}
                className="block text-white text-lg font-medium hover:text-yellow-200 transition cursor-pointer"
              >
                Services
              </motion.a>
              <motion.a
                onClick={() => {
                  navigate("/contact");
                  setIsOpen(false);
                }}
                initial={{ x: -20, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 3 * 0.1 }}
                className="block text-white text-lg font-medium hover:text-yellow-200 transition cursor-pointer"
              >
                Contact
              </motion.a>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
}
