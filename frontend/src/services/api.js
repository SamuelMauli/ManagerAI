// frontend/src/services/api.js

import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default {
  // Auth
  login: (credentials) => apiClient.post('/auth/login', credentials),
  getMe: () => apiClient.get('/users/me'),

  // Chat
  postChatMessage: (message) => apiClient.post('/chat', { message }),

  // --- ROTAS RESTAURADAS E ANTIGAS ---
  
  // YouTrack (incluindo Settings)
  getYoutrackProjects: () => apiClient.get('/youtrack/projects'),
  syncYoutrack: () => apiClient.post('/youtrack/sync'),
  getYouTrackSettings: () => apiClient.get('/settings/youtrack'), // Supondo esta rota
  saveYouTrackSettings: (settings) => apiClient.post('/settings/youtrack', settings), // Supondo esta rota
  
  // Tasks
  getTasks: (params) => apiClient.get('/tasks', { params }),
  getFilterData: () => apiClient.get('/tasks/filters'), // Supondo esta rota

  // Google & Email (incluindo Settings)
  getGoogleAuthUrl: () => apiClient.get('/google/auth-url'),
  handleGoogleCallback: (code) => apiClient.get(`/google/callback?code=${code}`),
  syncGoogleEmails: () => apiClient.post('/google/sync-emails'),
  getSyncedEmails: () => apiClient.get('/google/emails'),
  getEmailSettings: () => apiClient.get('/settings/email'), // Supondo esta rota
  saveEmailSettings: (settings) => apiClient.post('/settings/email', settings), // Supondo esta rota

  // --- NOVAS ROTAS ---

  // Jobs
  syncCalendar: () => apiClient.post('/jobs/calendar/sync'),
  runYouTrackJob: () => apiClient.post('/jobs/youtrack/sync'), // Mapeando para a rota de sync
  runEmailJob: () => apiClient.post('/jobs/email/sync'), // Mapeando para a rota de sync

  // Dashboard
  getProjectDashboard: (projectId) => apiClient.get(`/dashboard/project/${projectId}`),

  // Calendar
  getCalendarEvents: () => apiClient.get('/calendar/events'), // Supondo esta rota

  // Reports
  generateTasksByProjectReport: (data) => apiClient.post('/reports/tasks-by-project', data),
};