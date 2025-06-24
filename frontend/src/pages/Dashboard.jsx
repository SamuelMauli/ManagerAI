import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { BarChart, Mail, CheckSquare, LoaderCircle } from 'lucide-react';
import { getDashboardStats, getSummarizedEmails } from '../services/api';

const StatCard = ({ icon, label, value, color, isLoading }) => (
  <motion.div
    className="transform rounded-2xl border border-white/10 bg-dark-card/60 p-6 shadow-lg backdrop-blur-lg transition-transform hover:-translate-y-1"
    whileHover={{ scale: 1.05 }}
  >
    <div className="flex items-center justify-between">
      <p className="text-md font-medium text-dark-text-secondary">{label}</p>
      <div className={`rounded-full bg-${color}-500/20 p-2`}>
        {icon}
      </div>
    </div>
    <div className="mt-2 text-4xl font-bold text-dark-text">
        {isLoading ? <LoaderCircle className="h-8 w-8 animate-spin" /> : value}
    </div>
  </motion.div>
);

const Dashboard = () => {
  const { t } = useTranslation();
  const [stats, setStats] = useState({ unread_emails: 0, pending_tasks: 0, active_projects: 0 });
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const statsRes = await getDashboardStats();
        setStats(statsRes.data);
        const emailsRes = await getSummarizedEmails();
        setEmails(emailsRes.data);
      } catch (error) {
        console.error("Failed to fetch dashboard data:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

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
          value={stats.unread_emails}
          icon={<Mail className="h-6 w-6 text-blue-400" />}
          color="blue"
          isLoading={loading}
        />
        <StatCard
          label={t('dashboard.pendingTasks')}
          value={stats.pending_tasks}
          icon={<CheckSquare className="h-6 w-6 text-emerald-400" />}
          color="emerald"
          isLoading={loading}
        />
        <StatCard
          label={t('dashboard.activeProjects')}
          value={stats.active_projects}
          icon={<BarChart className="h-6 w-6 text-violet-400" />}
          color="violet"
          isLoading={loading}
        />
      </div>

      <div className="rounded-2xl border border-white/10 bg-dark-card/60 p-6 shadow-lg backdrop-blur-lg">
        <h2 className="text-xl font-bold text-dark-text">{t('dashboard.activityFeed')}</h2>
        {loading ? (
            <p className="text-dark-text-secondary mt-2">Loading recent emails...</p>
        ) : (
            <ul className="mt-4 space-y-4">
                {emails.map(email => (
                    <li key={email.id} className="p-3 rounded-lg bg-dark-primary/50">
                        <p className="font-semibold text-dark-text">{email.subject}</p>
                        <p className="text-sm text-dark-text-secondary">From: {email.sender}</p>
                        <p className="mt-1 text-sm text-dark-text">{email.summary}</p>
                    </li>
                ))}
            </ul>
        )}
      </div>
    </div>
  );
};

export default Dashboard;