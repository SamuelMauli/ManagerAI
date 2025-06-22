import Sidebar from './Sidebar';
import { Outlet } from 'react-router-dom';
import SettingsModal from '../ui/SettingsModal'; // Importar o Modal

const Layout = () => {
  return (
    <div className="relative flex min-h-screen bg-light-background dark:bg-dark-background">
      <Sidebar />
      <main className="flex-1 p-4 sm:p-6 md:p-8">
        <Outlet />
      </main>
      
      {/* O Modal de configurações será renderizado aqui */}
      <SettingsModal />
    </div>
  );
};

export default Layout;