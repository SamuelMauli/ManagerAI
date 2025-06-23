import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api', // Your backend API URL
});

// We configure the token in AuthContext, but you could also add interceptors here
// to handle token refresh or global error handling in the future.

export default api;