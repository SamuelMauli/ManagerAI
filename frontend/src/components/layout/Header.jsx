// frontend/src/components/layout/Header.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from '../ui/dropdown-menu';
import { Button } from '../ui/button';
import { CircleUser, Settings, LogOut } from 'lucide-react';
import ThemeSwitcher from '../ui/ThemeSwitcher';
import SettingsModal from '../ui/SettingsModal'; // Importe o SettingsModal

const Header = () => {
  const navigate = useNavigate();
  const [showSettingsModal, setShowSettingsModal] = useState(false); // Estado para o modal de configurações

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <header className="flex items-center h-16 px-4 border-b bg-background md:px-6">
      <div className="flex items-center w-full gap-4 md:gap-2 lg:gap-4">
        <div className="w-full" />
        <ThemeSwitcher />
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="secondary" size="icon" className="rounded-full">
              <CircleUser className="w-5 h-5" />
              <span className="sr-only">Toggle user menu</span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>Minha Conta</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={() => {
              // console.log("Configurações clicado!"); // Linha de depuração, pode remover
              setShowSettingsModal(true);
            }}>
              <Settings className="w-4 h-4 mr-2" />
              Configurações
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={handleLogout}>
              <LogOut className="w-4 h-4 mr-2" />
              Sair
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      {/* Renderiza o SettingsModal se showSettingsModal for true */}
      {showSettingsModal && (
        <SettingsModal show={showSettingsModal} onClose={() => setShowSettingsModal(false)} />
      )}
    </header>
  );
};

export default Header;