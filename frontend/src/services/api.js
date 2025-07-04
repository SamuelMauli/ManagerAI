import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('accessToken');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            localStorage.removeItem('accessToken');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export const auth = {
    googleLogin: (code) => api.post('/auth/google/callback', { code }),
    getCurrentUser: () => api.get('/auth/me'),
};

export const dashboard = {
    getDashboardSummary: () => api.get('/dashboard/summary'),
    getUpcomingTasks: () => api.get('/dashboard/tasks/upcoming'),
    getRecentEmails: () => api.get('/dashboard/emails/recent'),
};

export const tasks = {
    getTasks: (status = null) => {
        const params = status !== null ? { completed: status } : {};
        return api.get('/tasks/', { params });
    },
    createTask: (taskData) => api.post('/tasks/', taskData),
    updateTask: (taskId, taskData) => api.put(`/tasks/${taskId}`, taskData),
    deleteTask: (taskId) => api.delete(`/tasks/${taskId}`),
};

export const emails = {
    syncEmails: () => api.post('/emails/sync'),
    getPaginatedEmails: (skip = 0, limit = 100) => api.get(`/emails/?skip=${skip}&limit=${limit}`),
    getUnreadEmails: (skip = 0, limit = 100) => api.get(`/emails/unread?skip=${skip}&limit=${limit}`),
    getEmailDetail: (emailId) => api.get(`/emails/${emailId}`),
    markEmailAsRead: (emailId) => api.post(`/emails/${emailId}/mark_as_read`),
    sendEmail: (emailData) => api.post('/emails/send', emailData),
    getEmailThread: (threadId) => api.get(`/emails/thread/${threadId}`),
};

export const calendar = {
    getTodayEvents: () => api.get('/calendar/today'),
    getCalendarEvents: () => api.get('/calendar/events'),
    createCalendarEvent: (eventData) => api.post('/calendar/events', eventData),
    updateCalendarEvent: (eventId, eventData) => api.put(`/calendar/events/${eventId}`, eventData),
};

export const chat = {
    sendMessage: (message) => api.post('/chat', { query: message }),
};

export const reports = {
    generateReport: (projectId, prompt) => api.post('/reports', { project_id: projectId, user_prompt: prompt }),
};

export const youtrack = {
    getProjects: () => api.get('/youtrack/projects'),
    getIssues: (projectId) => api.get(`/youtrack/issues/${projectId}`),
    getBoards: (projectId) => api.get(`/youtrack/projects/${projectId}/boards`),
    getIssues: (projectShortName) => api.get(`/youtrack/issues/${projectShortName}`),
    getBoards: (projectId) => api.get(`/youtrack/projects/${projectId}/boards`),
};

export const settings = {
    updateYouTrackSettings: (settingsData) => api.post('/settings/youtrack', settingsData),
    updateEmailSettings: (settingsData) => api.post('/settings/email', settingsData),
};

export const drive = {
    searchFiles: (query, maxResults = 10) => api.get(`/drive/files?query=${query}&max_results=${maxResults}`),
    getFileContent: (fileId) => api.get(`/drive/files/${fileId}/content`),
    createFile: (fileName, mimeType, content) => api.post('/drive/files', { file_name: fileName, mime_type: mimeType, content: content }),
};

export default api;