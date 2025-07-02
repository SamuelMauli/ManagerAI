import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import Chat from './pages/Chat';
import Emails from './pages/Emails';
import Tasks from './pages/Tasks';
import Calendar from './pages/Calendar';
import { UIProvider } from './context/UIContext';
import CalendarPage from './pages/CalendarPage';
import ReportsPage from './pages/ReportsPage';

function App() {
  return (
    <Router>
      <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
        <div className="flex h-screen bg-background text-foreground">
          {isAuthenticated && <Sidebar />}
          <main className="flex-1 overflow-y-auto">
            {isAuthenticated && <Header />}
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
              <Route path="/chat" element={<PrivateRoute><Chat /></PrivateRoute>} />
              <Route path="/calendar" element={<PrivateRoute><CalendarPage /></PrivateRoute>} />
              <Route path="/reports" element={<PrivateRoute><ReportsPage /></PrivateRoute>} />
              <Route path="/settings" element={<PrivateRoute><Settings /></PrivateRoute>} />
            </Routes>
          </main>
        </div>
      </ThemeProvider>
    </Router>
  );
}

export default App;