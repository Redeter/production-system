import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

// Создаём экземпляр axios с базовым URL
const apiService = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Сгенерировать новые значения для системы
export const generateValues = async () => {
  try {
    const res = await apiService.get('/api/generate-values');
    return res.data;
  } catch (error) {
    console.error('Error generating values:', error);
    return { success: false, error: error.message };
  }
};

// Рассчитать систему с текущими параметрами
export const calculate = async (data) => {
  try {
    console.log('Sending calculation request:', data);
    const res = await apiService.post('/api/calculate', data);
    console.log('Calculation response:', res.data);
    return res.data;
  } catch (error) {
    console.error('Error calculating:', error);
    return { success: false, error: error.message };
  }
};

// Убрал getDefaultCoefficients, так как он больше не нужен

export { apiService };