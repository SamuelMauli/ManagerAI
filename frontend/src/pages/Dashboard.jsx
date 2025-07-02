import React, { useState, useEffect, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import api from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Briefcase, Calendar, Mail, CheckCircle, Clock } from 'lucide-react';
import CalendarWidget from '../components/dashboard/CalendarWidget';
import ActivityFeed from '../components/dashboard/ActivityFeed';

const Dashboard = () => {
  const { t } = useTranslation();
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await api.getYoutrackProjects();
        setProjects(response.data);
        if (response.data.length > 0) {
          setSelectedProject(response.data[0].id);
        }
      } catch (error) {
        console.error("Failed to fetch projects", error);
      }
    };
    fetchProjects();
  }, []);

  const fetchDashboardData = useCallback(async () => {
    if (!selectedProject) return;
    setLoading(true);
    try {
      const response = await api.getProjectDashboard(selectedProject);
      setDashboardData(response.data);
    } catch (error) {
      console.error("Failed to fetch dashboard data", error);
      setDashboardData(null);
    } finally {
      setLoading(false);
    }
  }, [selectedProject]);

  useEffect(() => {
    fetchDashboardData();
  }, [fetchDashboardData]);

  const chartData = dashboardData?.task_counts_by_status.map(item => ({
    name: item.status,
    count: item.count,
  })) || [];

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">{t('dashboard.title')}</h1>
        <div className="w-64">
          <Select onValueChange={setSelectedProject} value={selectedProject}>
            <SelectTrigger>
              <SelectValue placeholder={t('dashboard.select_project')} />
            </SelectTrigger>
            <SelectContent>
              {projects.map((p) => (
                <SelectItem key={p.id} value={p.id}>{p.name}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      {loading && <p>{t('loading')}...</p>}
      
      {dashboardData && !loading && (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{t('dashboard.total_tasks')}</CardTitle>
              <Briefcase className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{dashboardData.total_tasks}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{t('dashboard.unresolved_tasks')}</CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{dashboardData.unresolved_tasks}</div>
            </CardContent>
          </Card>
        </div>
      )}

      <div className="grid gap-6 md:grid-cols-2">
        {dashboardData && !loading && (
          <Card>
            <CardHeader>
              <CardTitle>{t('dashboard.tasks_by_status')}</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="count" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        )}
        <Card>
          <CardHeader>
            <CardTitle>{t('dashboard.upcoming_events')}</CardTitle>
          </CardHeader>
          <CardContent>
            <CalendarWidget />
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
            <CardTitle>{t('dashboard.activity_feed')}</CardTitle>
        </CardHeader>
        <CardContent>
            <ActivityFeed />
        </CardContent>
      </Card>

    </div>
  );
};

export default Dashboard;