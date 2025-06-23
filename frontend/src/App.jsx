import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { UIProvider } from './context/UIContext';

// Import Layout and Pages
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import Emails from './pages/Emails';
import Tasks from './pages/Tasks';
import Calendar from './pages/Calendar';
import Chat from './pages/Chat';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import './i18n';

// A protected route component that redirects to login if not authenticated
const ProtectedRoute = ({ children }) => {
  const { token } = useAuth();
  if (!token) {
    // Redirect them to the /login page, but save the current location they were
    // trying to go to. This allows us to redirect them back after login.
    return <Navigate to="/login" replace />;
  }
  return children;
};

// The main application structure
const AppContent = () => {
  const { token } = useAuth();
  return (
    <Router>
      <Routes>
        <Route path="/login" element={token ? <Navigate to="/" /> : <LoginPage />} />
        <Route path="/register" element={token ? <Navigate to="/" /> : <RegisterPage />} />
        
        {/* Protected Routes */}
        <Route 
          path="/*"
          element={
            <ProtectedRoute>
              <Layout>
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/emails" element={<Emails />} />
                  <Route path="/tasks" e   lement={<Tasks />} />
                  <Route path="/calendar" element={<Calendar />} />
                  <Route path="/chat" element={<Chat />} />
                   {/* Fallback for any other protected route */}
                  <Route path="*" element={<Navigate to="/" />} />
                </Routes>
              </Layout>
            </ProtectedRoute>
          } 
        />
      </Routes>
    </Router>
  );
};


function App() {
  return (
    <UIProvider>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </UIProvider>
  );
}

export default App;