export default function App() {
  return (
    <div
      style={{
        fontFamily: "Arial, sans-serif",
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background: "#0a0a0a",
        color: "#00ffae",
        fontSize: "2rem",
        flexDirection: "column",
        gap: "1rem",
      }}
    >
      <div>✅ MyCryptoFI toimii!</div>
      <div style={{ fontSize: "1rem", opacity: 0.8 }}>
        Tämä on testiversio. Sivun rakennus onnistui.
      </div>
    </div>
  );
}
