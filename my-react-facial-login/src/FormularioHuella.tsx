import React, { useState } from "react";

const API_BASE = "http://localhost:8000"; // Cambia el puerto si tu backend es diferente

const FormularioHuella: React.FC = () => {
  const [nombre, setNombre] = useState("");
  const [resultado, setResultado] = useState("");
  const [calidad, setCalidad] = useState<number | null>(null);
  const [score, setScore] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);

  const handleInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    setNombre(e.target.value);
  };

  const guardarHuella = async () => {
    if (!nombre.trim()) return alert("Debes ingresar un nombre");

    setLoading(true);
    setResultado("🖐️ Capturando huella para guardar...");
    setScore(null);
    setCalidad(null);

    try {
      const res = await fetch(`${API_BASE}/huella/guardar`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre })
      });

      const data = await res.json();

      if (!res.ok) throw new Error(data.detail || "Error desconocido");

      setResultado(data.mensaje);
      setCalidad(data.calidad);
    } catch (err: any) {
      setResultado("❌ Error al guardar: " + err.message);
    } finally {
      setLoading(false);
    }
  };

const verificarHuella = async () => {
  if (!nombre.trim()) return alert("Debes ingresar el nombre a verificar");

  setLoading(true);
  setResultado("🖐️ Capturando huella para verificar...");
  setScore(null);
  setCalidad(null);

  try {
    const res = await fetch(`${API_BASE}/huella/verificar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nombre })  // Asegúrate de pasar el nombre correctamente
    });

    const data = await res.json();

    if (!res.ok) {
      // Mostrar detalles del error si no es OK
      throw new Error(data.detail || "Error desconocido");
    }

    setResultado(data.resultado || data.mensaje);
    setScore(data.score ?? null);
    setCalidad(data.calidad ?? null);

  } catch (err: any) {
    console.error("Error al verificar huella:", err);  // Imprime el error en la consola
    setResultado("❌ Error al verificar: " + err.message);
  } finally {
    setLoading(false);
  }
};

  return (
    <div style={{ maxWidth: 400, margin: "0 auto", padding: "1rem", border: "1px solid #ccc", borderRadius: 8 }}>
      <h2>Verificación Biométrica</h2>

      <input
        type="text"
        placeholder="Nombre del usuario"
        value={nombre}
        onChange={handleInput}
        style={{ width: "100%", padding: "0.5rem", marginBottom: "1rem" }}
      />

      <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem" }}>
        <button onClick={guardarHuella} disabled={loading}>
          Guardar huella
        </button>
        <button onClick={verificarHuella} disabled={loading}>
          Verificar huella
        </button>
      </div>

      {loading && <p>⌛ Procesando...</p>}

      <div>
        <strong>Resultado:</strong> <p>{resultado}</p>
        {calidad !== null && <p>🧪 Calidad: {calidad}</p>}
        {score !== null && <p>📊 Similitud: {score}</p>}
      </div>
    </div>
  );
};

export default FormularioHuella;

