import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { BarChart, Mail, CheckSquare } from 'lucide-react';

// Um componente reutilizável para nossos cartões de estatísticas
const StatCard = ({ icon, label, value, color }) => (
  <motion.div
    className="transform rounded-2xl border border-white/10 bg-dark-card/60 p-6 shadow-lg backdrop-blur-lg transition-transform hover:-translate-y-1"
    whileHover={{ scale: 1.05 }}
  >
    <div className="flex items-center justify-between">
      <p className="text-md font-medium text-dark-text-secondary">{label}</p>
      {/* A cor do ícone é passada como propriedade */}
      <div className={`rounded-full bg-${color}-500/20 p-2`}>
        {icon}
      </div>
    </div>
    <p className="mt-2 text-4xl font-bold text-dark-text">{value}</p>
  </motion.div>
);

const Dashboard = () => {
  const { t } = useTranslation();
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-extrabold tracking-tight text-dark-text">
          {t('sidebar.dashboard')}
        </h1>
        <p className="mt-2 text-lg text-dark-text-secondary">
          {t('dashboard.welcome')}
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <StatCard
          label={t('dashboard.unreadEmails')}
          value="12"
          icon={<Mail className="h-6 w-6 text-blue-400" />}
          color="blue"
        />
        <StatCard
          label={t('dashboard.pendingTasks')}
          value="5"
          icon={<CheckSquare className="h-6 w-6 text-emerald-400" />}
          color="emerald"
        />
        <StatCard
          label={t('dashboard.activeProjects')}
          value="3"
          icon={<BarChart className="h-6 w-6 text-violet-400" />}
          color="violet"
        />
      </div>

      <div className="rounded-2xl border border-white/10 bg-dark-card/60 p-6 shadow-lg backdrop-blur-lg">
        <h2 className="text-xl font-bold text-dark-text">{t('dashboard.activityFeed')}</h2>
        <p className="mt-2 text-dark-text-secondary">{t('common.featureComingSoon')}</p>
      </div>
    </div>
  );
};

export default Dashboard;