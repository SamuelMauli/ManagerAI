import { AnimatePresence, motion } from 'framer-motion';
import { useLocation, Outlet } from 'react-router-dom';
import { useUI } from '../../context/UIContext';
import Header from './Header';
import Sidebar from './Sidebar';
import SettingsModal from '../ui/SettingsModal';

const Layout = () => {
  const { isSidebarCollapsed } = useUI();
  const location = useLocation();

  const mainContentStyle = {
    transition: 'margin-left 0.3s ease-in-out',
    marginLeft: isSidebarCollapsed ? '5rem' : '16rem', // 80px ou 256px
  };

  return (
    <div className="relative min-h-screen bg-light-background dark:bg-dark-background">
      {/* A Sidebar agora tem uma posição fixa e o conteúdo principal flui ao lado */}
      <Sidebar />
      
      <div
        className="flex flex-col md:ml-[16rem]" // O margin left padrão para desktop
        style={isSidebarCollapsed ? { marginLeft: '5rem' } : { marginLeft: '16rem' }}
      >
        {/* O Header fica dentro da área de conteúdo principal */}
        <Header />

        {/* Animação de transição de página */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8">
          <AnimatePresence mode="wait">
            <motion.div
              key={location.pathname}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
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