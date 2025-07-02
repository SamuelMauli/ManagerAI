import React from 'react';
import { useGoogleLogin } from '@react-oauth/google';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';

// Importando componentes de UI do seu projeto
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';

// Componente para o ícone do Google
const GoogleIcon = (props) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 48 48"
    width="24px"
    height="24px"
    {...props}
  >
    <path
      fill="#FFC107"
      d="M43.611,20.083H42V20H24v8h11.303c-1.649,4.657-6.08,8-11.303,8c-6.627,0-12-5.373-12-12s5.373-12,12-12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24s8.955,20,20,20s20-8.955,20-20C44,22.659,43.862,21.35,43.611,20.083z"
    />
    <path
      fill="#FF3D00"
      d="M6.306,14.691l6.571,4.819C14.655,15.108,18.961,12,24,12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C16.318,4,9.656,8.337,6.306,14.691z"
    />
    <path
      fill="#4CAF50"
      d="M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.19-5.238C29.211,35.091,26.715,36,24,36c-5.222,0-9.657-3.356-11.303-7.962l-6.571,4.819C9.656,39.663,16.318,44,24,44z"
    />
    <path
      fill="#1976D2"
      d="M43.611,20.083H42V20H24v8h11.303c-0.792,2.237-2.231,4.166-4.087,5.571l6.19,5.238C42.021,35.596,44,30.138,44,24C44,22.659,43.862,21.35,43.611,20.083z"
    />
  </svg>
);


const Login = () => {
  const navigate = useNavigate();

  // A lógica de autenticação permanece a mesma que já funciona
  const googleLogin = useGoogleLogin({
    onSuccess: async (codeResponse) => {
      try {
        const toastId = toast.loading('Verificando credenciais...');
        const { data } = await axios.post(
          'http://localhost:8000/auth/google/callback',
          { code: codeResponse.code }
        );
        toast.success('Login bem-sucedido!', { id: toastId });
        localStorage.setItem('accessToken', data.access_token);
        navigate('/dashboard', { replace: true });
      } catch (error) {
        const errorMessage = error.response?.data?.detail || 'Falha no login. Tente novamente.';
        toast.error(errorMessage);
        console.error('Falha no Login:', errorMessage);
      }
    },
    onError: (error) => {
        toast.error('O login com o Google falhou.');
        console.error('Falha no Login do Google:', error);
    },
    flow: 'auth-code',
  });

  return (
    <main className="flex items-center justify-center min-h-screen bg-gray-50 dark:bg-gray-900 p-4">
      <Card className="w-full max-w-md shadow-lg">
        <CardHeader className="text-center space-y-2">
          {/* Você pode adicionar sua logo aqui se desejar */}
          <h1 className="text-2xl font-bold tracking-tight text-gray-900 dark:text-gray-50">
            Manager AI
          </h1>
          <CardDescription>
            Faça login com sua conta Google para continuar
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button 
            variant="outline" 
            className="w-full h-12 text-base" 
            onClick={() => googleLogin()}
          >
            <GoogleIcon className="mr-3" />
            Entrar com o Google
          </Button>
        </CardContent>
      </Card>
    </main>
  );
};

export default Login;