import { useTranslation } from 'react-i18next';
import { NavLink } from 'react-router-dom';
// CORREÇÃO: Adicionado 'MessageCircle' na linha de importação abaixo
import { LayoutDashboard, Mail, CheckSquare, Calendar, MessageCircle, Settings, PanelLeftClose, PanelLeftOpen, X, Bot } from 'lucide-react';
import { useUI } from '../../context/UIContext';
import { motion } from 'framer-motion';

const Sidebar = () => {
  const { t } = useTranslation();
  const {
    isSidebarCollapsed,
    toggleSidebar,
    isMobileMenuOpen,
    toggleMobileMenu,
    openSettingsModal,
  } = useUI();

  // O array de navegação agora pode usar 'MessageCircle' sem erros
  const navItems = [
    { name: t('sidebar.dashboard'), icon: LayoutDashboard, href: '/' },
    { name: t('sidebar.chat'), icon: MessageCircle, href: '/chat' },
    { name: t('sidebar.emails'), icon: Mail, href: '/emails' },
    { name: t('sidebar.tasks'), icon: CheckSquare, href: '/tasks' },
    { name: t('sidebar.calendar'), icon: Calendar, href: '/calendar' },
  ];

  const baseLinkClasses = "flex items-center p-3 my-1 rounded-lg text-dark-text-secondary hover:bg-dark-accent hover:text-white transition-colors duration-200";
  const activeLinkClasses = "!text-white bg-dark-accent/80 shadow-lg";
  
  const sidebarClasses = `
    fixed inset-y-0 left-0 z-50 flex h-screen flex-col 
    bg-light-primary dark:bg-dark-primary 
    text-light-text dark:text-dark-text 
    border-r border-white/10
    p-4 transition-all duration-300 ease-in-out
    ${isSidebarCollapsed ? 'w-20' : 'w-64'}
    ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'}
    md:translate-x-0
  `;

  return (
    <>
      {/* Overlay para fechar o menu no mobile */}
      {isMobileMenuOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black/60 md:hidden"
          onClick={toggleMobileMenu}
        ></div>
      )}

      <aside className={sidebarClasses}>
        {/* Cabeçalho da Sidebar */}
        <div className="flex items-center justify-between pb-8">
            <div className={`flex items-center gap-2 overflow-hidden`}>
                <Bot className="text-dark-accent flex-shrink-0" size={28}/>
                <span className={`text-xl font-bold whitespace-nowrap transition-opacity duration-200 ${isSidebarCollapsed ? 'opacity-0' : 'opacity-100'}`}>
                    ManagerAI
                </span>
            </div>
           
           <button onClick={toggleMobileMenu} className="p-1 md:hidden">
             <X size={24} />
           </button>
        </div>

        {/* Navegação Principal */}
        <nav className="flex-1">
          <ul>
            {navItems.map((item) => (
              <li key={item.name}>
                <NavLink
                  to={item.href}
                  end
                  className={({ isActive }) => `${baseLinkClasses} ${isActive ? activeLinkClasses : ''}`}
                  onClick={() => isMobileMenuOpen && toggleMobileMenu()}
                  title={isSidebarCollapsed ? item.name : ''}
                >
                  <item.icon className="mr-4 flex-shrink-0" size={22} />
                  <span className={`whitespace-nowrap transition-opacity duration-200 ${isSidebarCollapsed ? 'opacity-0' : 'opacity-100'}`}>
                    {item.name}
                  </span>
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>

        {/* Rodapé da Sidebar */}
        <div>
           <div className="hidden md:block border-t border-white/10 pt-4">
                <button 
                  onClick={toggleSidebar} 
                  className={`${baseLinkClasses} w-full`}
                  title={isSidebarCollapsed ? t('sidebar.expand') : t('sidebar.collapse')}
                >
                    {isSidebarCollapsed ? (
                        <PanelLeftOpen size={22} className="mx-auto" />
                    ) : (
                        <>
                            <PanelLeftClose size={22} className="mr-4 flex-shrink-0" />
                            <span className="whitespace-nowrap">{t('sidebar.collapse')}</span>
                        </>
                    )}
                </button>
           </div>

          <button onClick={openSettingsModal} className={`${baseLinkClasses} w-full mt-2`}>
            <Settings className="mr-4 flex-shrink-0" size={22} />
            <span className={`whitespace-nowrap transition-opacity duration-200 ${isSidebarCollapsed ? 'opacity-0' : 'opacity-100'}`}>
              {t('sidebar.settings')}
            </span>
          </button>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;