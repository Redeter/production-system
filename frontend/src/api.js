import axios from 'axios';

const API_URL = 'https://production-system.onrender.com/api';

export const generateValues = async () => {
    const res = await axios.get(`${API_URL}/generate-values`);
    return res.data;
}

export const runSystem = async (data) => {
    const res = await axios.post(`${API_URL}/calculate`, data);
    return res.data;
}

export const loadDefaultCoefficients = async () => {
    const res = await axios.get(`${API_URL}/default-coefficients`);
    return res.data;
}
