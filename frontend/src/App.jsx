import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import Chat from './pages/Chat';
import Emails from './pages/Emails';
import Tasks from './pages/Tasks';
import Calendar from './pages/Calendar';
import { UIProvider } from './context/UIContext';

function App() {
  return (
    <UIProvider>
      <Router>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/chat" element={<Chat />} />
            <Route path="/emails" element={<Emails />} />
            <Route path="/tasks" element={<Tasks />} />
            <Route path="/calendar" element={<Calendar />} />
          </Route>
        </Routes>
      </Router>
    </UIProvider>
  );
}

export default App;