import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { I18nextProvider } from 'react-i18next';
import { Toaster } from 'react-hot-toast';

// Config e Contexto
import i18n from './i18n';
import { UIProvider } from './context/UIContext';

// Componentes
import Layout from './components/layout/Layout'; // Certifique-se que o caminho está correto
import PrivateRoute from './components/auth/PrivateRoute';
import SettingsModal from './components/ui/SettingsModal';

// Páginas
import Dashboard from './pages/Dashboard';
import Tasks from './pages/Tasks';
import Emails from './pages/Emails';
import CalendarPage from './pages/CalendarPage';
import Chat from './pages/Chat';
import ReportsPage from './pages/ReportsPage';
import Login from './pages/Login';
import GoogleAuthCallback from './pages/GoogleAuthCallback';
import LoginCallback from './pages/LoginCallback';
import DrivePage from './pages/DrivePage'; // Importe a nova página do Drive

const App = () => {
    const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;

    return (
        <GoogleOAuthProvider clientId={googleClientId}>
            <I18nextProvider i18n={i18n}>
                <UIProvider>
                    <Router>
                        <Toaster position="top-center" reverseOrder={false} />

                        <Routes>
                            {/* Rotas Públicas */}
                            <Route path="/login" element={<Login />} />
                            <Route path="/google/callback" element={<GoogleAuthCallback />} />
                            <Route path="/login/callback" element={<LoginCallback />} />

                            {/* Rotas Privadas agrupadas sob o PrivateRoute e Layout */}
                            <Route element={<PrivateRoute />}>
                                <Route element={<Layout />}> {/* <-- Reintroduza o Layout AQUI! */}
                                    <Route index element={<Navigate to="/dashboard" replace />} /> {/* Adicionado novamente */}
                                    <Route path="dashboard" element={<Dashboard />} />
                                    <Route path="tasks" element={<Tasks />} />
                                    <Route path="emails" element={<Emails />} />
                                    <Route path="calendar" element={<CalendarPage />} />
                                    <Route path="chat" element={<Chat />} />
                                    <Route path="reports" element={<ReportsPage />} />
                                    <Route path="drive" element={<DrivePage />} /> {/* Nova rota do Drive */}
                                </Route>
                            </Route>

                            {/* Redireciona qualquer rota não encontrada para a raiz */}
                            <Route path="*" element={<Navigate to="/" replace />} /> {/* Adicionado novamente */}
                        </Routes>
                        <SettingsModal />
                    </Router>
                </UIProvider>
            </I18nextProvider>
        </GoogleOAuthProvider>
    );
};

export default App;