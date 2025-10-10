import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const generateValues = async () => {
    const res = await axios.get(`${API_URL}/generate`);
    return res.data;
}

export const runSystem = async (data) => {
    const res = await axios.post(`${API_URL}/run`, data);
    return res.data;
}