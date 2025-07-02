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
        const apiBaseUrl = import.meta.env.VITE_API_URL;

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

        localStorage.setItem('token', data.access_token);
        toast.success('Login bem-sucedido!');
        navigate('/dashboard', { replace: true });

      } catch (error) {
        toast.error(`Falha no Login: ${error.message}`);
      }
    },
    flow: 'auth-code',
  });

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-96">
        <div className="flex justify-center mb-6">
          <h1 className="text-2xl font-semibold text-gray-800">Manager AI</h1>
        </div>
        <p className="text-center text-gray-600 mb-4">Faça login para continuar</p>
        <button
          onClick={() => handleLogin()}
          className="flex items-center justify-center w-full py-3 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
        >
          <img src={googleIcon} alt="Google Icon" className="mr-2 h-5 w-5" />
          <span className="text-sm font-medium text-gray-700">Entrar com o Google</span>
        </button>
      </div>
    </div>
  );
};

export default Login
