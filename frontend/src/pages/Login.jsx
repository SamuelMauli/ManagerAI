// frontend/src/pages/Login.jsx
import React, { useEffect } from 'react';
import { useGoogleLogin } from '@react-oauth/google';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import { motion } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import { Bot, LogIn } from 'lucide-react';
import api from '../services/api';

const Login = () => {
  const navigate = useNavigate();
  const { t } = useTranslation();

  useEffect(() => {
    // Se já houver um token, redireciona para o painel
    if (localStorage.getItem('token')) {
      navigate('/dashboard');
    }
  }, [navigate]);

  // Função para lidar com o sucesso do login no Google
  const handleGoogleLoginSuccess = async (tokenResponse) => {
    try {
      // Envia o 'code' para o backend
      const { data } = await api.post('/auth/google', {
        code: tokenResponse.code,
      });

      // Salva o token JWT no localStorage
      localStorage.setItem('token', data.access_token);
      
      // Configura o cabeçalho de autorização para futuras requisições
      api.defaults.headers.common['Authorization'] = `Bearer ${data.access_token}`;
      
      toast.success(t('login.success', 'Login bem-sucedido!'));
      navigate('/dashboard');

    } catch (error) {
      console.error('Google Login Failed:', error);
      toast.error(t('login.error', 'Falha no login com o Google.'));
    }
  };

  // Hook da biblioteca do Google para iniciar o fluxo de login
  const login = useGoogleLogin({
    onSuccess: handleGoogleLoginSuccess,
    flow: 'auth-code', // Essencial para este fluxo
    onError: () => toast.error(t('login.error', 'Falha no login com o Google.')),
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
          {t('login.welcomeTitle', 'Bem-vindo ao ManagerAI')}
        </h1>
        <p className="mt-3 text-lg text-dark-text-secondary">
          {t('login.welcomeSubtitle', 'Seu assistente pessoal com IA para otimizar seu trabalho.')}
        </p>
        <div className="mt-10">
          <button
            onClick={() => login()}
            className="inline-flex w-full items-center justify-center gap-3 rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white transition-transform hover:scale-105 hover:bg-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-dark-background"
          >
            <LogIn size={20} />
            {t('login.googleButton', 'Entrar com Google')}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Login;