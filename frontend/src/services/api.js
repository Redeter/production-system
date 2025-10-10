import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

// Создаём экземпляр axios с базовым URL
const apiService = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Получить коэффициенты по умолчанию
export const getDefaultCoefficients = async () => {
  const res = await apiService.get('/api/default-coefficients');
  return res.data;
};

// Сгенерировать новые значения для системы
export const generateValues = async () => {
  const res = await apiService.get('/api/generate-values');
  return res.data;
};

// Рассчитать систему с текущими параметрами
export const calculate = async (data) => {
  const res = await apiService.post('/api/calculate', data);
  return res.data;
};

export { apiService };
