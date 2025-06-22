import { createContext, useState, useContext } from 'react';

const UIContext = createContext();

export const UIProvider = ({ children }) => {
  // Estado para a sidebar no DESKTOP (recolhida ou não)
  const [isSidebarCollapsed, setSidebarCollapsed] = useState(false);
  
  // NOVO: Estado para a sidebar no MOBILE (aberta ou fechada)
  const [isMobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Estado para o modal
  const [isSettingsModalOpen, setSettingsModalOpen] = useState(false);

  const toggleSidebar = () => setSidebarCollapsed(prevState => !prevState);
  const toggleMobileMenu = () => setMobileMenuOpen(prevState => !prevState);
  
  const openSettingsModal = () => setSettingsModalOpen(true);
  const closeSettingsModal = () => {
    setSettingsModalOpen(false);
    setMobileMenuOpen(false); // Fecha o menu mobile se abrir o modal
  }


  const value = {
    isSidebarCollapsed,
    toggleSidebar,
    isMobileMenuOpen,
    toggleMobileMenu,
    isSettingsModalOpen,
    openSettingsModal,
    closeSettingsModal,
  };

  return <UIContext.Provider value={value}>{children}</UIContext.Provider>;
};

export const useUI = () => {
  return useContext(UIContext);
};