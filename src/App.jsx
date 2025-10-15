import React from "react";
import { motion } from "framer-motion";

export default function App() {
  return (
    <div className="min-h-screen bg-black flex flex-col items-center justify-center text-center text-gray-200 font-mono">
      <motion.h1
        className="text-5xl md:text-7xl font-bold mb-8 text-cyan-400 drop-shadow-[0_0_20px_#00ffff]"
        initial={{ opacity: 0, y: -40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
      >
        MyCryptoFI
      </motion.h1>

      <motion.p
        className="max-w-xl text-lg md:text-xl text-gray-400"
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5, duration: 1 }}
      >
        Suomen oma tekoäly-ohjattu krypto-opas ja bottiekosysteemi.  
        <br />
        <span className="text-cyan-300">Automatisoi. Analysoi. Toimi.</span>
      </motion.p>

      <motion.a
        href="https://twitter.com"
        target="_blank"
        rel="noopener noreferrer"
        whileHover={{ scale: 1.1, textShadow: "0 0 25px #00ffff" }}
        className="mt-10 px-8 py-3 border border-cyan-400 rounded-lg text-cyan-300 hover:bg-cyan-900/20 transition-all"
      >
        Seuraa päivityksiä
      </motion.a>
    </div>
  );
}