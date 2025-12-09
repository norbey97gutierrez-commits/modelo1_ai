import { useState } from 'react';
import './App.css';

function App() {
  // 1. Estados para manejar la entrada, la respuesta y el estado de carga
  const [prompt, setPrompt] = useState('');
  const [respuesta, setRespuesta] = useState('La respuesta de la IA aparecerá aquí.');
  const [cargando, setCargando] = useState(false);

  // 2. Función para manejar la solicitud al backend
  const manejarEnvio = async (e) => {
    e.preventDefault(); // Evita que la página se recargue

    // Verificamos que no esté vacío y no esté cargando
    if (!prompt || cargando) return;

    setCargando(true); // Iniciamos el estado de carga
    setRespuesta('Generando respuesta...'); // Indicamos al usuario que estamos esperando

    try {
      // 3. Solicitud POST al endpoint /generate de tu FastAPI
      const urlBackend = 'http://localhost:8000/generate'; // ¡Asegúrate que coincida con tu backend!
      
      const response = await fetch(urlBackend, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Opcional: Para permitir CORS si fuera necesario, aunque Fetch suele manejarlo
        },
        // 4. Enviamos el JSON con la estructura que espera tu FastAPI ({"prompt": "..."})
        body: JSON.stringify({ prompt: prompt }),
      });

      if (!response.ok) {
        throw new Error(`Error en el servidor: ${response.status}`);
      }

      // 5. Obtenemos la respuesta JSON del backend
      const data = await response.json();
      
      // 6. Actualizamos el estado con la respuesta de la IA
      setRespuesta(data.respuesta_generada);

    } catch (error) {
      console.error('Hubo un problema con la operación fetch:', error);
      setRespuesta(`Error al conectar con el servidor: ${error.message}`);
    } finally {
      setCargando(false); // Siempre detenemos el estado de carga
    }
  };

  return (
    <div className="contenedor-ia">
      <h1>🤖 Asistente de IA (Python Expert)</h1>
      <p>Conectado a tu Backend de FastAPI con LangChain.</p>

      {/* Formulario de entrada */}
      <form onSubmit={manejarEnvio} className="formulario">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Escribe tu consulta sobre programación Python..."
          rows="5"
          disabled={cargando}
        />
        <button type="submit" disabled={cargando}>
          {cargando ? 'Cargando...' : 'Preguntar a la IA'}
        </button>
      </form>

      {/* Área de respuesta */}
      <div className="respuesta-container">
        <h2>✨ Respuesta</h2>
        <p className="respuesta-texto">{respuesta}</p>
      </div>
    </div>
  );
}

export default App;