import React from "react";
import "./index.css";

export default function App() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-black via-gray-900 to-black text-gray-100 flex flex-col items-center justify-center p-8">
      <h1 className="text-4xl md:text-6xl font-bold mb-6 text-center text-blue-400 drop-shadow-[0_0_10px_#1e90ff]">
        MyCryptoFI
      </h1>
      <p className="max-w-xl text-center text-gray-300 text-lg">
        Krypto-opas suomalaisille — tietoa, uutisia ja käytännön vinkkejä
        digitaalisesta taloudesta.
      </p>
      <div className="mt-12 text-sm text-gray-500">
        © 2025 MyCryptoFI — Rakennettu tekoäly-pohjaisesti.
      </div>
    </main>
  );
}
