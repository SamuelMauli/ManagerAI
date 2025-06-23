import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { UIProvider } from './context/UIContext';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import Emails from './pages/Emails';
import Tasks from './pages/Tasks';
import Calendar from './pages/Calendar';
import Chat from './pages/Chat';
import './i18n';

const AppRoutes = () => (
  <Routes>
    <Route path="/" element={<Dashboard />} />
    <Route path="/emails" element={<Emails />} />
    <Route path="/tasks" element={<Tasks />} />
    <Route path="/calendar" element={<Calendar />} />
    <Route path="/chat" element={<Chat />} />
    <Route path="*" element={<Navigate to="/" />} />
  </Routes>
);

function App() {
  return (
    <UIProvider>
      <Router>
        <Layout>
          <AppRoutes />
        </Layout>
      </Router>
    </UIProvider>
  );
}

export default App;