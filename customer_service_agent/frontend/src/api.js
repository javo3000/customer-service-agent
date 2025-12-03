import axios from 'axios';

const api = axios.create({
    baseURL: '/', // Proxy handles the redirection to localhost:8000
    headers: {
        'Content-Type': 'application/json',
    },
});

export const askAgent = async (question, chatHistory = []) => {
    try {
        const response = await api.post('/ask', {
            question,
            chat_history: chatHistory,
        });
        return response.data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
};
