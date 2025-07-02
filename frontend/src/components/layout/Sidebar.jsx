import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Bot, LogOut } from 'lucide-react';

import { 
  LayoutDashboard, 
  MessageSquare, 
  Calendar, 
  FileText, 
  Settings as SettingsIcon 
} from 'lucide-react';

const Sidebar = () => {
  const { t } = useTranslation();
  const location = useLocation();

  const navItems = [
    { href: '/', icon: LayoutDashboard, label: t('sidebar.dashboard') },
    { href: '/chat', icon: MessageSquare, label: t('sidebar.chat') },
    { href: '/calendar', icon: Calendar, label: t('sidebar.calendar') },
    { href: '/reports', icon: FileText, label: t('sidebar.reports') },
    { href: '/settings', icon: SettingsIcon, label: t('sidebar.settings') },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <aside className="flex h-full w-64 flex-col border-r bg-background p-4">
      <div className="mb-8 flex items-center gap-2">
        <Bot size={32} className="text-primary" />
        <h1 className="text-2xl font-bold">ManagerAI</h1>
      </div>

      <nav className="flex-1 space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.href}
            to={item.href}
            className={`flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:bg-muted hover:text-foreground
              ${isActive(item.href) ? 'bg-primary text-primary-foreground hover:bg-primary/90 hover:text-primary-foreground' : ''}`}
          >
            <item.icon className="h-5 w-5" />
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="mt-auto">
        <button className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:bg-muted hover:text-foreground">
          <LogOut className="h-5 w-5" />
          {t('sidebar.logout')}
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;