import { Menu } from 'lucide-react';
import { useUI } from '../../context/UIContext';
import ThemeSwitcher from '../ui/ThemeSwitcher';

const Header = () => {
  const { toggleMobileMenu } = useUI();

  return (
    <header className="sticky top-0 z-10 flex h-16 items-center justify-between border-b border-white/10 bg-light-card/80 px-4 shadow-sm backdrop-blur-xl dark:bg-dark-card/80 md:justify-end md:px-8">
      {/* Botão do menu mobile (só aparece em telas pequenas) */}
      <button
        onClick={toggleMobileMenu}
        className="p-2 text-light-text-secondary dark:text-dark-text-secondary md:hidden"
        aria-label="Abrir menu"
      >
        <Menu size={24} />
      </button>

      {/* Itens do Header (ex: busca, perfil, etc.) podem ir aqui */}
      <div className="flex items-center gap-4">
        <ThemeSwitcher />
        {/* Futuramente: <UserMenu /> */}
      </div>
    </header>
  );
};

export default Header;