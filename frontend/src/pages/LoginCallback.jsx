// frontend/src/pages/LoginCallback.jsx
import React, { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const LoginCallback = () => {
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    // Extrai o token dos parâmetros da URL
    const params = new URLSearchParams(location.search);
    const token = params.get('token');

    if (token) {
      // Salva o token para uso futuro em chamadas de API
      localStorage.setItem('user_token', token);
      // Redireciona o usuário para o dashboard ou página principal
      navigate('/dashboard'); 
    } else {
      // Se não houver token, houve um erro. Redirecione para a página de login.
      navigate('/login');
    }
  }, [location, navigate]);

  return (
    <div>
      <p>Autenticando...</p>
    </div>
  );
};

export default LoginCallback;