import React from 'react';

const ChatInput = ({ prompt, setPrompt, manejarEnvio, cargando }) => (
    <div className="input-wrapper">
        <form onSubmit={manejarEnvio} className="input-form">
            <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Mensaje al experto en Python..."
                rows="1"
                disabled={cargando}
            />
            <button type="submit" disabled={cargando}>
                {cargando ? 'Cargando...' : '↑'}
            </button>
        </form>
    </div>
);

export default ChatInput;