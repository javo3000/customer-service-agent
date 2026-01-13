import axios from 'axios';

const api = axios.create({
    baseURL: '/', // Proxy handles the redirection to localhost:8000
    headers: {
        'Content-Type': 'application/json',
    },
});

export const askAgent = async (question, chatHistory = [], onChunk) => {
    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question,
                chat_history: chatHistory,
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');

            // Keep the last part (potentially incomplete line) in the buffer
            buffer = lines.pop();

            for (const line of lines) {
                const trimmedLine = line.trim();
                if (!trimmedLine) continue;

                if (trimmedLine.startsWith('data: ')) {
                    try {
                        const data = JSON.parse(trimmedLine.slice(6));
                        onChunk(data);
                    } catch (e) {
                        console.error("Error parsing JSON chunk:", trimmedLine, e);
                    }
                }
            }
        }

        // Process any remaining data in buffer if it's a complete SSE line
        if (buffer.trim().startsWith('data: ')) {
            try {
                const data = JSON.parse(buffer.trim().slice(6));
                onChunk(data);
            } catch (e) { /* ignore partial final data */ }
        }
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
};
