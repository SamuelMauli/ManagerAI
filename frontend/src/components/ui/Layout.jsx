import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';
import SettingsModal from '../ui/SettingsModal';
import { useUI } from '../../context/UIContext';

const Layout = () => {
    const { isSidebarCollapsed } = useUI();
    
    const paddingLeft = isSidebarCollapsed === undefined ? '256px' : (isSidebarCollapsed ? '80px' : '256px');

    return (
        <div className="flex h-screen bg-dark-background">
            <Sidebar />
            <div 
              className={`flex-1 flex flex-col transition-all duration-300 ease-in-out md:pl-[var(--sidebar-width)]`}
              style={{ '--sidebar-width': paddingLeft }}
            >
                <Header />
                <main className="flex-1 overflow-y-auto p-4 md:p-8">
                    <Outlet />
                </main>
            </div>
            <SettingsModal />
        </div>
    );
};

export default Layout;