import React, { createContext, useState, useContext, useEffect } from 'react';
import api from '../services/api'; // We will create this api service

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem('authToken'));
  // You can also store user info here
  // const [user, setUser] = useState(null); 

  useEffect(() => {
    if (token) {
      localStorage.setItem('authToken', token);
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      localStorage.removeItem('authToken');
      delete api.defaults.headers.common['Authorization'];
    }
  }, [token]);

  const login = async (email, password) => {
    const response = await api.post('/token', { username: email, password });
    if (response.data.access_token) {
      setToken(response.data.access_token);
    }
    return response;
  };

  const register = async(fullName, email, password) => {
    return await api.post('/users/', { full_name: fullName, email, password });
  }

  const logout = () => {
    setToken(null);
    // You might want to navigate the user to the login page here
    // window.location.href = '/login';
  };

  const value = { token, login, logout, register };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to easily use the auth context in other components
export const useAuth = () => {
  return useContext(AuthContext);
};