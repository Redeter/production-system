import axios from 'axios';

const API_BASE = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
});

export const apiService = {
  generateValues: () => api.get('/generate-values'),
  calculate: (data) => api.post('/calculate', data),
  getDefaultCoefficients: () => api.get('/default-coefficients')
};

export default api;