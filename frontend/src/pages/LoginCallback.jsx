import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import toast from 'react-hot-toast';

const LoginCallback = () => {
  const [error, setError] = useState('');
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    // Pega o parâmetro 'code' da URL
    const code = new URLSearchParams(location.search).get('code');

    if (code) {
      const exchangeCodeForToken = async () => {
        try {
          const toastId = toast.loading('Autenticando...');
          
          const response = await axios.post('http://localhost:8000/auth/google/callback', {
            code: code,
          });
          
          const { access_token } = response.data;
          
          if (access_token) {
            // Salva o token no localStorage
            localStorage.setItem('accessToken', access_token);
            toast.success('Login realizado com sucesso!', { id: toastId });
            
            // Navega para o dashboard, substituindo a rota atual
            navigate('/dashboard', { replace: true });
          } else {
            throw new Error('Token de acesso não recebido.');
          }

        } catch (err) {
          const errorMessage = err.response?.data?.detail || 'Falha na autenticação. Tente novamente.';
          console.error('Erro no callback de login:', errorMessage);
          setError(errorMessage);
          toast.error(errorMessage);
          // Redireciona de volta para a página de login em caso de erro
          navigate('/login', { replace: true });
        }
      };

      exchangeCodeForToken();
    } else {
        setError('Nenhum código de autorização encontrado.');
        navigate('/login', { replace: true });
    }
  }, [location, navigate]);

  if (error) {
    return <div>Erro: {error}</div>;
  }

  return (
    <div>
      <h2>Autenticando, por favor aguarde...</h2>
    </div>
  );
};

export default LoginCallback;