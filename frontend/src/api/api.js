import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Fetches the list of tasks with optional filters
export const getTasks = (filters = {}) => {
  const params = new URLSearchParams(filters);
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
  // CORREÇÃO: Alterado de '/jobs/youtrack/run' para '/jobs/youtrack/sync'
  return api.post('/jobs/youtrack/sync');
};

// Runs the Email synchronization job
export const runEmailJob = () => {
  // CORREÇÃO: Alterado de '/jobs/email/run' para '/jobs/email/sync'
  return api.post('/jobs/email/sync');
};

// Fetches dashboard statistics
export const getDashboardStats = () => {
  return api.get('/dashboard/stats');
};

export default api;