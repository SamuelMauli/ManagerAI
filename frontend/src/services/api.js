import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/',
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
  register: (userData) => apiClient.post('/auth/register', userData),
  googleAuthCallback: (code) => apiClient.post('/auth/google/callback', { code }),
  getCurrentUser: () => apiClient.get('/auth/me'),

  // Chat
  postChatMessage: (message) => apiClient.post('/chat', { message }),

  // --- ROTAS RESTAURADAS E ANTIGAS ---
  
  // YouTrack (incluindo Settings)
  getYoutrackProjects: () => apiClient.get('/youtrack/projects'),
  syncYoutrack: () => apiClient.post('/youtrack/sync'),
  getYouTrackSettings: () => apiClient.get('/settings/youtrack'), // Supondo esta rota
  saveYouTrackSettings: (settings) => apiClient.post('/settings/youtrack', settings), // Supondo esta rota
  
  // Tasks
  getTasks: (params = {}) => apiClient.get('/tasks/', { params }), // Adicione esta linha
  createTask: (taskData) => apiClient.post('/tasks/', taskData), // Adicione esta linha
  updateTask: (taskId, taskData) => apiClient.put(`/tasks/${taskId}`, taskData), // Adicione esta linha
  deleteTask: (taskId) => apiClient.delete(`/tasks/${taskId}`), // Adicione esta linha


  // Google & Email (incluindo Settings)
  syncEmails: () => apiClient.post('/emails/sync'),
  // Endpoint para buscar e-mails do banco de dados
  getSyncedEmails: () => apiClient.get('/emails/'),
  // Endpoint para buscar e-mails não lidos
  getUnreadEmails: () => apiClient.get('/emails/unread'),
  // Endpoint para marcar e-mail como lido
  markEmailAsRead: (emailId) => apiClient.post(`/emails/${emailId}/mark_as_read`),
  // Endpoint para buscar detalhes de um email específico
  getEmailDetails: (emailId) => apiClient.get(`/emails/${emailId}`),

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