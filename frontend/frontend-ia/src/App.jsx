import React from 'react';
// Importamos los componentes de presentación
import Mensaje from './components/Mensaje';
import ChatInput from './components/ChatInput';
import Bienvenida from './components/Bienvenida';
import ChatFooter from './components/ChatFooter';

// Importamos el hook de lógica
import { useChatLogic } from './hooks/useChatLogic';
import './App.css';

function App() {
  const {
    prompt,
    setPrompt,
    conversacion,
    cargando,
    chatEndRef,
    manejarEnvio,
  } = useChatLogic();

  const isInitialState = conversacion.length === 0;

  return (
    <div className="chat-layout">

      {/* ------------------------------------- */}
      {/* Componente de Bienvenida */}
      {/* ------------------------------------- */}
      {isInitialState && <Bienvenida />}

      {/* ------------------------------------- */}
      {/* Contenedor de la Conversación */}
      {/* ------------------------------------- */}
      <div className="conversacion-container">
        {conversacion.map((msg, index) => (
          <Mensaje key={index} texto={msg.texto} tipo={msg.tipo} />
        ))}
        {/* Referencia de Scroll */}
        <div ref={chatEndRef} />
      </div>

      {/* ------------------------------------- */}
      {/* Componente de Input */}
      {/* ------------------------------------- */}
      <ChatInput
        prompt={prompt}
        setPrompt={setPrompt}
        manejarEnvio={manejarEnvio}
        cargando={cargando}
      />

      {/* ------------------------------------- */}
      {/* Componente de Footer */}
      {/* ------------------------------------- */}
      <ChatFooter />

    </div>
  );
}

export default App;