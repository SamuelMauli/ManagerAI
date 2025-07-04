// frontend/src/pages/Login.jsx

import React from 'react';
import { useGoogleLogin } from '@react-oauth/google';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
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
    {/* SVG paths... */}
  </svg>
);

const Login = () => {
  const navigate = useNavigate();

  // Define os scopes que o seu backend espera.
  // Estes devem corresponder à variável GOOGLE_SCOPES no seu backend.
  const scopes = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/drive'
  ].join(' ');

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
    scope: scopes,
  });

  return (
    <main className="flex items-center justify-center min-h-screen bg-gray-50 dark:bg-gray-900 p-4">
      <Card className="w-full max-w-md shadow-lg">
        <CardHeader className="text-center space-y-2">
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