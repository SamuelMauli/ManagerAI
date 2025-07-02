import { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';

const LoginCallback = () => {
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const code = params.get('code');

    if (!code) {
      toast.error('Falha no login: Código de autorização não encontrado.');
      navigate('/login');
      return;
    }

    const exchangeCodeForToken = async () => {
      try {
        const apiBaseUrl = import.meta.env.VITE_API_URL;
        const response = await fetch(`${apiBaseUrl}/auth/google/callback`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ code }),
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.detail || 'Erro ao autenticar com o servidor.');
        }

        // AQUI ESTÁ A MUDANÇA CRÍTICA
        // Vamos salvar o token de acesso do Google que será usado nas chamadas de API
        localStorage.setItem('google_access_token', data.access_token);
        
        toast.success('Login realizado com sucesso!');
        navigate('/dashboard', { replace: true });

      } catch (error) {
        toast.error(`Erro: ${error.message}`);
        navigate('/login', { replace: true });
      }
    };

    exchangeCodeForToken();
  }, [location, navigate]);

  return (
    <div className="flex items-center justify-center h-screen">
      <p>Autenticando, por favor aguarde...</p>
    </div>
  );
};

export default LoginCallback
