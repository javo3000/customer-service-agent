import React, { useState } from 'react';
import { Send, Loader2 } from 'lucide-react';

const InputArea = ({ onSend, isLoading }) => {
    const [input, setInput] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (input.trim() && !isLoading) {
            onSend(input);
            setInput('');
        }
    };

    return (
        <div className="fixed bottom-0 left-0 w-full bg-dark-bg/80 backdrop-blur-lg border-t border-white/10 p-4 z-50">
            <div className="max-w-4xl mx-auto">
                <form onSubmit={handleSubmit} className="relative flex items-center">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask about orders, policies, or general inquiries..."
                        disabled={isLoading}
                        className="w-full bg-dark-input text-white rounded-xl py-4 pl-6 pr-14 focus:outline-none focus:ring-2 focus:ring-primary/50 border border-white/5 placeholder-gray-400 shadow-lg transition-all"
                    />
                    <button
                        type="submit"
                        disabled={!input.trim() || isLoading}
                        className={`absolute right-2 p-2 rounded-lg transition-all ${input.trim() && !isLoading
                                ? 'bg-primary hover:bg-primary-dark text-white shadow-lg shadow-primary/30'
                                : 'bg-transparent text-gray-500 cursor-not-allowed'
                            }`}
                    >
                        {isLoading ? <Loader2 className="animate-spin" size={20} /> : <Send size={20} />}
                    </button>
                </form>
                <p className="text-center text-xs text-gray-500 mt-2">
                    AI Agent can make mistakes. Please verify important information.
                </p>
            </div>
        </div>
    );
};

export default InputArea;
