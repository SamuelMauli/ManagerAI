import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// --- CHAT ---
// Adicionada a função para enviar mensagens ao chat
export const postChatMessage = (message) => {
  return api.post('/chat', { message });
};

// --- DASHBOARD ---
// Fetches dashboard statistics
export const getDashboardStats = () => {
  return api.get('/dashboard/stats');
};

// Adicionada a função para buscar e-mails sumarizados
export const getSummarizedEmails = () => {
  return api.get('/emails/summarized'); 
};


// --- TASKS ---
// Fetches the list of tasks with optional filters
export const getTasks = (filters = {}) => {
  // Remove chaves vazias para não poluir a URL
  const cleanedFilters = Object.fromEntries(
    Object.entries(filters).filter(([_, v]) => v != null && v !== '')
  );
  const params = new URLSearchParams(cleanedFilters);
  return api.get(`/tasks?${params.toString()}`);
};

// Fetches the filter data for the tasks page
export const getFilterData = () => {
  return Promise.all([
    api.get('/projects'),
    api.get('/tasks/assignees'),
    api.get('/tasks/statuses'),
  ]);
};

// --- SETTINGS & JOBS ---
// Saves YouTrack settings
export const saveYouTrackSettings = (settings) => {
  return api.post('/settings/youtrack', settings);
};

// Fetches YouTrack settings
export const getYouTrackSettings = () => {
  return api.get('/settings/youtrack');
};

// Saves Email settings
export const saveEmailSettings = (settings) => {
  return api.post('/settings/gmail', settings);
};

// Fetches Email settings
export const getEmailSettings = () => {
  return api.get('/settings/gmail');
};

// Runs the YouTrack synchronization job
export const runYouTrackJob = () => {
  return api.post('/jobs/youtrack/sync');
};

// Runs the Email synchronization job
export const runEmailJob = () => {
  return api.post('/jobs/email/sync');
};

export default api;