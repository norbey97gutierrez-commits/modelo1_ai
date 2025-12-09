import { useState, useRef, useEffect } from 'react';

// Conexion con la URL del backend
const API_URL = 'http://localhost:8000/generate';

/**
 * Hook para manejar toda la lógica de la conversación del chat.
 */
export const useChatLogic = () => {
  const [prompt, setPrompt] = useState('');
  const [conversacion, setConversacion] = useState([]);
  const [cargando, setCargando] = useState(false);

  // Lógica de scroll
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [conversacion]);
  
  // ----------------------------------------------------
  // Función central: Manejo del envío y la comunicación con la API
  // ----------------------------------------------------
  const manejarEnvio = async (e) => {
    e.preventDefault();
    const preguntaUsuario = prompt.trim();

    if (!preguntaUsuario || cargando) return;

    setCargando(true);
    setPrompt('');

    // Agregamos el mensaje del usuario
    const nuevoMensajeUsuario = { texto: preguntaUsuario, tipo: 'usuario' };
    setConversacion(prev => [...prev, nuevoMensajeUsuario]);

    // Mensaje de carga
    const mensajeCarga = { texto: 'Generando respuesta...', tipo: 'ia', id: 'cargando' };
    setConversacion(prev => [...prev, mensajeCarga]);

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: preguntaUsuario }),
      });

      if (!response.ok) {
        throw new Error(`Error en el servidor: ${response.status}`);
      }

      const data = await response.json();
      const respuestaIA = data.respuesta_generada;

      const nuevoMensajeIA = { texto: respuestaIA, tipo: 'ia' };

      // Reemplazamos el mensaje de carga con la respuesta
      setConversacion(prev =>
        prev.map(msg => (msg.id === 'cargando' ? nuevoMensajeIA : msg))
      );

    } catch (error) {
      console.error('Hubo un problema con la operación fetch:', error);
      const mensajeError = {
        texto: `Error: ${error.message}. Asegúrate de que el Backend está corriendo y CORS está configurado.`,
        tipo: 'ia'
      };

      // 4. Reemplazamos el mensaje de carga con el error
      setConversacion(prev =>
        prev.map(msg => (msg.id === 'cargando' ? mensajeError : msg))
      );

    } finally {
      setCargando(false);
    }
  };

  // El hook expone solo las variables y funciones que necesita el componente App
  return {
    prompt,
    setPrompt,
    conversacion,
    cargando,
    chatEndRef,
    manejarEnvio,
  };
};