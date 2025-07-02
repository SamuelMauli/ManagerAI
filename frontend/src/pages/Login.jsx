import { useGoogleLogin } from '@react-oauth/google';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import googleIcon from '../assets/google-icon.svg';

const Login = () => {
  const navigate = useNavigate();

  const handleLogin = useGoogleLogin({
    onSuccess: async (codeResponse) => {
      try {
        const code = codeResponse.code;
        const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

        const response = await fetch(`${apiBaseUrl}/auth/google/callback`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ code: code }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || 'Falha ao trocar código pelo token no backend.');
        }

        // AQUI ESTÁ A CORREÇÃO CRÍTICA
        // Salvamos o token com a chave que o Dashboard vai procurar
        localStorage.setItem('google_access_token', data.access_token);
        
        toast.success('Login bem-sucedido!');
        navigate('/dashboard', { replace: true });

      } catch (error) => {
        toast.error(`Falha no Login: ${error.message}`);
      }
    },
    flow: 'auth-code',
  });

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900">
      <div className="w-full max-w-sm p-8 space-y-6 bg-white rounded-lg shadow-md dark:bg-gray-800">
        <div className="text-center">
          <h1 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-gray-50">
            Manager.AI
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            Faça login para continuar
          </p>
        </div>
        <button
          onClick={() => handleLogin()}
          className="w-full inline-flex justify-center items-center gap-2 py-2.5 px-4 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:bg-gray-700 dark:text-gray-200 dark:border-gray-600 dark:hover:bg-gray-600"
        >
          <img src={googleIcon} alt="Google Icon" className="w-5 h-5" />
          Entrar com o Google
        </button>
      </div>
    </div>
  );
};

export default Login;