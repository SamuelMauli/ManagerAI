import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';

// Contexto e Componentes de Layout
import { UIProvider } from './context/UIContext';
import Layout from './components/layout/Layout';
import SettingsModal from './components/ui/SettingsModal';

// Páginas
import Login from './pages/Login';
import LoginCallback from './pages/LoginCallback'; // Componente crucial
import Dashboard from './pages/Dashboard';
import Chat from './pages/Chat';
import Tasks from './pages/Tasks';
import Emails from './pages/Emails';
import CalendarPage from './pages/CalendarPage';
import ReportsPage from './pages/ReportsPage';

/**
 * Protege uma rota, redirecionando para /login se não houver token.
 */
const PrivateRoute = ({ children }) => {
  // A chave 'token' deve ser a mesma usada no LoginCallback
  const token = localStorage.getItem('token'); 
  return token ? children : <Navigate to="/login" replace />;
};

function App() {
  return (
    <UIProvider>
      <Router>
        <Toaster position="top-center" reverseOrder={false} />
        
        <Routes>
          {/* Rotas Públicas */}
          <Route path="/login" element={<Login />} />
          <Route path="/login/callback" element={<LoginCallback />} />

          {/* Rotas Privadas aninhadas sob o Layout */}
          <Route 
            path="/" 
            element={
              <PrivateRoute>
                <Layout />
              </PrivateRoute>
            }
          >
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="chat" element={<Chat />} />
            <Route path="tasks" element={<Tasks />} />
            <Route path="emails" element={<Emails />} />
            <Route path="calendar" element={<CalendarPage />} />
            <Route path="reports" element={<ReportsPage />} />
          </Route>
          
          {/* Rota para lidar com caminhos não encontrados */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
        
        <SettingsModal />
      </Router>
    </UIProvider>
  );
}

export default App;