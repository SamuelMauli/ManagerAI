import React, { useEffect } from 'react';
import { useGoogleLogin } from '@react-oauth/google';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import api from '../api/api';
import { Bot, LogIn } from 'lucide-react';
import { useTranslation } from 'react-i18next';

const Login = () => {
  const navigate = useNavigate();
  const { t } = useTranslation();

  // Redireciona se o usuário já estiver logado
  useEffect(() => {
    if (localStorage.getItem('token')) {
      navigate('/dashboard');
    }
  }, [navigate]);

  const handleGoogleLoginSuccess = async (tokenResponse) => {
    try {
      // Envia o código de autorização para o backend
      const { data } = await api.post('/auth/google', {
        code: tokenResponse.code,
      });

      // Armazena o token JWT e redireciona para o dashboard
      localStorage.setItem('token', data.access_token);
      api.defaults.headers.common['Authorization'] = `Bearer ${data.access_token}`;
      toast.success(t('login.success'));
      navigate('/dashboard');

    } catch (error) {
      console.error('Google Login Failed:', error);
      toast.error(t('login.error'));
    }
  };

  const login = useGoogleLogin({
    onSuccess: handleGoogleLoginSuccess,
    flow: 'auth-code', // Usa o fluxo de código de autorização, que é mais seguro
    onError: () => toast.error(t('login.error')),
  });

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-dark-background p-4">
      <div className="w-full max-w-md text-center">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mx-auto mb-8 flex h-16 w-16 items-center justify-center rounded-full bg-dark-accent"
        >
          <Bot size={32} className="text-white" />
        </motion.div>
        <h1 className="text-4xl font-extrabold tracking-tight text-dark-text">
          {t('login.welcomeTitle')}
        </h1>
        <p className="mt-3 text-lg text-dark-text-secondary">
          {t('login.welcomeSubtitle')}
        </p>
        <div className="mt-10">
          <button
            onClick={() => login()}
            className="inline-flex w-full items-center justify-center gap-3 rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white transition-transform hover:scale-105 hover:bg-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-dark-background"
          >
            <LogIn size={20} />
            {t('login.googleButton')}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Login;