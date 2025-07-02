import React from 'react';
import { useTranslation } from 'react-i18next';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Bell } from 'lucide-react';

// Dados mocados para o feed de atividades
const activities = [
  { id: 1, type: 'task_completed', description: 'Tarefa "Implementar login" foi concluída.' },
  { id: 2, type: 'new_email', description: 'Você recebeu um novo e-mail de "cliente@example.com".' },
  { id: 3, type: 'meeting_soon', description: 'Reunião "Daily Standup" começa em 15 minutos.' },
];

const ActivityFeed = () => {
  const { t } = useTranslation();

  return (
    <div className="space-y-4">
      {activities.length > 0 ? (
        <ul className="space-y-3">
          {activities.map(activity => (
            <li key={activity.id} className="flex items-start gap-3">
              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/10">
                <Bell className="h-4 w-4 text-primary" />
              </div>
              <div className="flex-1">
                <p className="text-sm">{activity.description}</p>
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-sm text-muted-foreground">{t('dashboard.no_recent_activity')}</p>
      )}
    </div>
  );
};

export default ActivityFeed;

// Componentes UI básicos que podem estar em outros arquivos
// como /components/ui/card.jsx

const UiCard = ({ children, ...props }) => <div {...props}>{children}</div>;
const UiCardHeader = ({ children, ...props }) => <div {...props}>{children}</div>;
const UiCardTitle = ({ children, ...props }) => <h3 {...props}>{children}</h3>;
const UiCardContent = ({ children, ...props }) => <div {...props}>{children}</div>;

export { UiCard as Card, UiCardHeader as CardHeader, UiCardTitle as CardTitle, UiCardContent as CardContent };