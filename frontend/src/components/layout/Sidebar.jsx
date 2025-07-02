import { NavLink } from 'react-router-dom';
import { Home, Bot, CheckCircle, Mail, Calendar, BarChart2 } from 'lucide-react';

const navItems = [
  { to: '/dashboard', icon: Home, label: 'Dashboard' },
  { to: '/chat', icon: Bot, label: 'Chat IA' },
  { to: '/tasks', icon: CheckCircle, label: 'Tarefas' },
  { to: '/emails', icon: Mail, label: 'Emails' },
  { to: '/calendar', icon: Calendar, label: 'Calendário' },
  { to: '/reports', icon: BarChart2, label: 'Relatórios' },
];

const Sidebar = () => {
  const baseClasses = 'flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary';
  const activeClasses = 'bg-muted text-primary';

  return (
    <aside className="hidden w-64 border-r bg-background md:block">
      <div className="flex flex-col h-full">
        <div className="flex items-center h-16 px-6 border-b">
          <NavLink to="/" className="flex items-center gap-2 font-semibold">
            <Bot className="w-6 h-6" />
            <span>Manager.AI</span>
          </NavLink>
        </div>
        <nav className="flex-1 px-4 py-4">
          <ul className="space-y-1">
            {navItems.map((item) => (
              <li key={item.label}>
                <NavLink
                  to={item.to}
                  className={({ isActive }) => `${baseClasses} ${isActive ? activeClasses : ''}`}
                >
                  <item.icon className="w-4 h-4" />
                  {item.label}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </aside>
  );
};

export default Sidebar;