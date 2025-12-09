import React from 'react';

const Mensaje = ({ texto, tipo }) => (
    <div className={`mensaje mensaje--${tipo}`}>
        <div className="mensaje__avatar">
            {tipo === 'ia' ? '🤖' : '👤'}
        </div>
        <div className="mensaje__contenido">
            {tipo === 'ia' && <h2 className="mensaje__header-ia">Respuesta</h2>}
            <p className="mensaje__texto">{texto}</p>
        </div>
    </div>
);

export default Mensaje;