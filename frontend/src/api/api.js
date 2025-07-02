import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // URL base da sua API
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor de Requisição: Adiciona o token ao cabeçalho de cada requisição
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor de Resposta: Lida com erros globais, como o 401 Unauthorized
api.interceptors.response.use(
  (response) => {
    // Se a resposta for bem-sucedida, apenas a retorna
    return response;
  },
  (error) => {
    // Se o erro for 401, o token é inválido ou expirou
    if (error.response && error.response.status === 401) {
      // Limpa o token do localStorage
      localStorage.removeItem('accessToken');
      // Redireciona o usuário para a página de login
      // Usar window.location.href garante que o estado do React seja recarregado
      window.location.href = '/login';
    }
    // Rejeita a promessa para que o erro possa ser tratado localmente se necessário
    return Promise.reject(error);
  }
);

export default api;