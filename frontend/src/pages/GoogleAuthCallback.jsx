import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const GoogleAuthCallback = () => {
  const [error, setError] = useState(null);
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    // 1. Extrair o 'code' da URL
    const params = new URLSearchParams(location.search);
    const code = params.get('code');

    if (!code) {
      setError("Código de autorização do Google não encontrado.");
      return;
    }

    // 2. Enviar o 'code' para o backend
    const exchangeCodeForToken = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/auth/google/callback`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ code }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Falha na comunicação com o backend.');
        }

        // 3. Receber e salvar o token JWT
        const data = await response.json();
        localStorage.setItem('authToken', data.access_token);
        
        // 4. Redirecionar para a página principal
        navigate('/dashboard'); // ou para a rota que você quiser

      } catch (err) {
        setError(err.message);
      }
    };

    exchangeCodeForToken();

  }, [location, navigate]);

  return (
    <div>
      {error ? (
        <div>
          <h1>Erro de Autenticação</h1>
          <p>{error}</p>
          <button onClick={() => navigate('/login')}>Voltar para o Login</button>
        </div>
      ) : (
        <p>Autenticando, por favor aguarde...</p>
      )}
    </div>
  );
};

export default GoogleAuthCallback
