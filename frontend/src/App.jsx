import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import LoginCallback from './pages/LoginCallback';
import Dashboard from './pages/Dashboard';
import { Toaster } from 'react-hot-toast';
import { UIProvider } from './context/UIContext';
import Layout from './components/layout/Layout';
import Chat from './pages/Chat';
import CalendarPage from './pages/CalendarPage';
import ReportsPage from './pages/ReportsPage';
import SettingsModal from './components/ui/SettingsModal';
import Tasks from './pages/Tasks';
import Emails from './pages/Emails';

// Um componente simples para proteger rotas
const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <UIProvider>
      <Router>
        <Toaster position="top-center" reverseOrder={false} />
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/login/callback" element={<LoginCallback />} />
          <Route path="/" element={<PrivateRoute><Layout /></PrivateRoute>}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="chat" element={<Chat />} />
            <Route path="tasks" element={<Tasks />} />
            <Route path="emails" element={<Emails />} />
            <Route path="calendar" element={<CalendarPage />} />
            <Route path="reports" element={<ReportsPage />} />
          </Route>
        </Routes>
        <SettingsModal />
      </Router>
    </UIProvider>
  );
}

export default App;