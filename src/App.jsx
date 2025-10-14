import { Canvas } from "@react-three/fiber";
import { OrbitControls, Float, Html } from "@react-three/drei";
import { motion } from "framer-motion";
import "./index.css";

export default function App() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-black via-[#0b0f1a] to-black text-white">
      <div className="absolute inset-0 overflow-hidden">
        <Canvas camera={{ position: [0, 0, 5] }}>
          <ambientLight intensity={0.3} />
          <pointLight position={[10, 10, 10]} />
          <Float speed={3}>
            <mesh>
              <sphereGeometry args={[1.5, 64, 64]} />
              <meshStandardMaterial
                color="#00bfff"
                metalness={0.8}
                roughness={0.2}
                emissive="#0077ff"
                emissiveIntensity={0.6}
              />
            </mesh>
          </Float>
          <OrbitControls enableZoom={false} autoRotate />
        </Canvas>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1.5 }}
        className="relative z-10 text-center p-8 max-w-3xl"
      >
        <h1 className="text-4xl md:text-6xl font-bold mb-6 text-cyan-400 drop-shadow-[0_0_15px_#00bfff]">
          MyCryptoFI
        </h1>
        <p className="text-gray-300 text-lg">
          Krypto-opas suomalaisille — tietoa, uutisia ja käytännön vinkkejä
          digitaalisesta taloudesta.
        </p>
      </motion.div>

      <motion.div
        className="relative z-10 mt-12 p-8 backdrop-blur-md bg-white/5 rounded-2xl border border-white/10 shadow-[0_0_30px_#00bfff50]"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.2, duration: 1.5 }}
      >
        <h2 className="text-xl font-semibold mb-4 text-cyan-300">
          ⚡ Uusimmat kryptouutiset
        </h2>
        <p className="text-gray-400 text-sm">
          Päivitykset tulevat automaattisesti bottien kautta. Seuraa MyCryptoFI.
        </p>
      </motion.div>
    </div>
  );
}
