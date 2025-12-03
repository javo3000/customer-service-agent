import React, { useState } from 'react';
import { Send, Paperclip, Smile } from 'lucide-react';

const ChatInput = ({ onSend, isLoading }) => {
    const [input, setInput] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (input.trim() && !isLoading) {
            onSend(input);
            setInput('');
        }
    };

    return (
        <form onSubmit={handleSubmit} className="p-4 bg-dark-card border-t border-dark-border">
            <div className="relative flex items-center">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask anything ..."
                    className="w-full bg-dark-bg text-dark-text rounded-full py-3 pl-4 pr-24 focus:outline-none focus:ring-2 focus:ring-primary/50 border border-dark-border placeholder:text-dark-muted text-sm"
                    disabled={isLoading}
                />
                <div className="absolute right-2 flex items-center gap-1">
                    <button type="button" className="p-2 text-dark-muted hover:text-primary transition-colors">
                        <Paperclip size={18} />
                    </button>
                    <button type="button" className="p-2 text-dark-muted hover:text-primary transition-colors">
                        <Smile size={18} />
                    </button>
                    <button
                        type="submit"
                        disabled={!input.trim() || isLoading}
                        className="p-2 text-primary hover:text-primary-dark disabled:opacity-50 transition-colors"
                    >
                        <Send size={18} />
                    </button>
                </div>
            </div>
        </form>
    );
};

export default ChatInput;
