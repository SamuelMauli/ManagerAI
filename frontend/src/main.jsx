import React from 'react';
import ReactDOM from 'react-dom/client';
import { GoogleOAuthProvider } from '@react-oauth/google';
import App from './App';
import './index.css';

// Acessa a variável de ambiente com o prefixo VITE_
const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;

// Adicionamos um alerta para garantir que o problema seja visível
if (!GOOGLE_CLIENT_ID) {
  const errorMessage = "ERRO CRÍTICO: A variável VITE_GOOGLE_CLIENT_ID não foi encontrada. Verifique se o arquivo 'frontend/.env' existe e contém a variável corretamente.";
  alert(errorMessage);
  console.error(errorMessage);
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    {/* O provider só será renderizado se a chave existir */}
    {GOOGLE_CLIENT_ID ? (
      <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
        <App />
      </GoogleOAuthProvider>
    ) : (
      <div style={{ padding: '20px', backgroundColor: 'red', color: 'white', textAlign: 'center' }}>
        <h1>Erro de Configuração</h1>
        <p>A aplicação não pode ser iniciada. Verifique o console do navegador para mais detalhes.</p>
      </div>
    )}
  </React.StrictMode>
);