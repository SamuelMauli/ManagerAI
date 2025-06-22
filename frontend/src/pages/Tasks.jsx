import { useTranslation } from 'react-i18next';
import { PlusCircle } from 'lucide-react';

const Tasks = () => {
  const { t } = useTranslation();
  return (
    <div className="space-y-8">
      <div className="flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <h1 className="text-4xl font-extrabold tracking-tight text-dark-text">
            {t('sidebar.tasks')}
          </h1>
          <p className="mt-2 text-lg text-dark-text-secondary">
            {t('tasks.subtitle')}
          </p>
        </div>
        <button className="inline-flex items-center gap-2 rounded-lg bg-dark-accent px-4 py-2 font-semibold text-white transition-colors hover:bg-dark-accent-hover">
          <PlusCircle size={20} />
          {t('tasks.newButton')}
        </button>
      </div>
      <div className="flex min-h-[50vh] items-center justify-center rounded-2xl border border-white/10 bg-dark-card/60 p-6 text-center shadow-lg backdrop-blur-lg">
        <p className="text-dark-text-secondary">{t('common.contentPlaceholder')}</p>
      </div>
    </div>
  );
};

export default Tasks;