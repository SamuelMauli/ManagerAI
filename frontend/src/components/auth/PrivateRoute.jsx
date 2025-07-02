import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

const PrivateRoute = () => {
  // A chave 'accessToken' deve ser a mesma usada no LoginCallback
  const isAuthenticated = !!localStorage.getItem('accessToken');

  // Se estiver autenticado, renderiza o conteúdo da rota filha (usando <Outlet />)
  // Caso contrário, redireciona para a página de login
  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
};

export default PrivateRoute;