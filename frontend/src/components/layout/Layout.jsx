import { Outlet, useLocation } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import { useUI } from '../../context/UIContext';
import Sidebar from './Sidebar';
import Header from './Header';
import SettingsModal from '../ui/SettingsModal';

const Layout = () => {
  const { isSidebarCollapsed } = useUI();
  const location = useLocation();

  return (
    <div className="relative min-h-screen">
      <Sidebar />
      <div
        className="flex flex-1 flex-col transition-all duration-300 ease-in-out md:ml-[var(--sidebar-width)]"
        style={{ '--sidebar-width': isSidebarCollapsed ? '5rem' : '16rem' }}
      >
        <Header />
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
          <AnimatePresence mode="wait">
            <motion.div
              key={location.pathname}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -15 }}
              transition={{ duration: 0.25 }}
            >
              <Outlet />
            </motion.div>
          </AnimatePresence>
        </main>
      </div>
      <SettingsModal />
    </div>
  );
};

export default Layout;