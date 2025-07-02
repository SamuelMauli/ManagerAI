import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { PlusCircle, Filter } from 'lucide-react';
import api from '../services/api';
import toast from 'react-hot-toast';

const Tasks = () => {
  const { t } = useTranslation();

  const [tasks, setTasks] = useState([]);
  const [projects, setProjects] = useState([]);
  const [statuses, setStatuses] = useState([]);
  const [assignees, setAssignees] = useState([]);
  
  const [loading, setLoading] = useState(true);
  const [showFilters, setShowFilters] = useState(false);
  
  const [selectedProject, setSelectedProject] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('');
  const [selectedAssignee, setSelectedAssignee] = useState('');

  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const [projRes, assignRes, statRes] = await getFilterData();
        setProjects(projRes.data);
        setAssignees(assignRes.data);
        setStatuses(statRes.data);
      } catch (error) {
        console.error("Failed to fetch filter data", error);
        toast.error(t('tasks.errors.loadFilters'));
      }
    };
    fetchInitialData();
  }, [t]);

  useEffect(() => {
    const fetchTasks = async () => {
      setLoading(true);
      const filters = {
        project_id: selectedProject,
        status: selectedStatus,
        assignee: selectedAssignee,
      };
      
      try {
        const response = await getTasks(filters);
        setTasks(response.data);
      } catch (error) {
        console.error("Failed to fetch tasks", error);
        setTasks([]);
        toast.error(t('tasks.errors.loadTasks'));
      } finally {
        setLoading(false);
      }
    };
    fetchTasks();
  }, [selectedProject, selectedStatus, selectedAssignee, t]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <h1 className="text-4xl font-extrabold tracking-tight text-dark-text">
            {t('sidebar.tasks')}
          </h1>
          <p className="mt-2 text-lg text-dark-text-secondary">
            {t('tasks.subtitle')}
          </p>
        </div>
        <div className="flex items-center gap-2">
           <button 
             onClick={() => setShowFilters(!showFilters)}
             className="inline-flex items-center gap-2 rounded-lg bg-dark-card px-4 py-2 font-semibold text-white transition-colors hover:bg-dark-border"
           >
            <Filter size={20} />
            {t('common.filters')}
          </button>
          <button className="inline-flex items-center gap-2 rounded-lg bg-dark-accent px-4 py-2 font-semibold text-white transition-colors hover:bg-dark-accent-hover">
            <PlusCircle size={20} />
            {t('tasks.newButton')}
          </button>
        </div>
      </div>

      {showFilters && (
        <div className="grid grid-cols-1 gap-4 rounded-xl border border-white/10 bg-dark-card/60 p-4 sm:grid-cols-2 md:grid-cols-3">
          <div>
            <label className="text-sm font-medium text-dark-text-secondary">{t('tasks.project')}</label>
            <select
              value={selectedProject}
              onChange={(e) => setSelectedProject(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-600 bg-dark-card p-2 text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            >
              <option value="">{t('common.all')}</option>
              {projects.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
            </select>
          </div>
          <div>
             <label className="text-sm font-medium text-dark-text-secondary">{t('tasks.status')}</label>
             <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-600 bg-dark-card p-2 text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            >
              <option value="">{t('common.all')}</option>
              {statuses.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
          <div>
             <label className="text-sm font-medium text-dark-text-secondary">{t('tasks.assignee')}</label>
             <select
               value={selectedAssignee}
               onChange={(e) => setSelectedAssignee(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-600 bg-dark-card p-2 text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            >
              <option value="">{t('common.all')}</option>
              {assignees.map(a => <option key={a} value={a}>{a || t('common.unassigned')}</option>)}
            </select>
          </div>
        </div>
      )}
      
      <div className="min-h-[50vh] rounded-2xl border border-white/10 bg-dark-card/60 p-6 shadow-lg backdrop-blur-lg">
        {loading ? (
          <div className="flex h-full items-center justify-center text-dark-text-secondary">
            {t('common.loading')}
          </div>
        ) : tasks.length > 0 ? (
          <ul className="space-y-4">
            {tasks.map(task => (
              <li key={task.id} className="rounded-lg bg-dark-card p-4 transition-colors hover:bg-dark-border">
                <div className="flex items-center justify-between">
                    <p className="font-bold text-dark-text">{task.title}</p>
                    <span className="rounded-full bg-dark-accent px-2 py-1 text-xs font-semibold text-white">{task.status}</span>
                </div>
                <p className="mt-2 text-sm text-dark-text-secondary">
                  {t('tasks.assignee')}: <span className="font-medium text-white">{task.assignee || t('common.unassigned')}</span>
                </p>
              </li>
            ))}
          </ul>
        ) : (
          <div className="flex h-full items-center justify-center text-dark-text-secondary">
            <p>{t('tasks.noTasksFound')}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Tasks;