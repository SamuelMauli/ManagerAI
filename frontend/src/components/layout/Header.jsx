import { Menu } from 'lucide-react';
import { useUI } from '../../context/UIContext';
import ThemeSwitcher from '../ui/ThemeSwitcher';

const Header = () => {
  const { toggleMobileMenu } = useUI();

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-light-border/80 bg-light-background/80 px-4 shadow-sm backdrop-blur-xl dark:border-dark-border/80 dark:bg-dark-background/80 md:justify-end md:px-8">
      <button onClick={toggleMobileMenu} className="p-2 text-light-text-secondary dark:text-dark-text-secondary md:hidden" aria-label="Abrir menu">
        <Menu size={24} />
      </button>
      <div className="flex items-center gap-4">
        <ThemeSwitcher />
        {/* Futuramente aqui: <UserMenu /> */}
      </div>
    </header>
  );
};

export default Header;