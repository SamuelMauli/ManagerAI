import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api', // Your backend API URL
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to add the auth token to every request
api.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, error => {
    return Promise.reject(error);
});


// --- Dashboard ---
export const getDashboardStats = () => api.get('/dashboard/stats');
export const getSummarizedEmails = () => api.get('/dashboard/summarized-emails');

// --- Chat ---
export const postChatMessage = (message) => api.post('/chat/message', { message });


// --- Settings ---
export const getYouTrackSettings = () => api.get('/settings/youtrack');
export const saveYouTrackSettings = (data) => api.post('/settings/youtrack', data);
export const getGmailSettings = () => api.get('/settings/gmail');
export const saveGmailSettings = (data) => api.post('/settings/gmail', data);

// --- Jobs ---
export const runYouTrackJob = () => api.post('/jobs/youtrack/run');
export const runEmailJob = () => api.post('/jobs/email/run');


export default api;