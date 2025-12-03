import React from 'react';
import { X, Bot } from 'lucide-react';

const ChatHeader = ({ onClose }) => {
    return (
        <div className="bg-primary p-4 flex items-center justify-between shadow-md z-10">
            <div className="flex items-center gap-3">
                <div className="bg-white/20 p-2 rounded-full">
                    <Bot className="text-white" size={24} />
                </div>
                <div>
                    <h3 className="text-white font-semibold text-lg">AlFin</h3>
                    <p className="text-primary-light text-xs">24*7 Support Bot</p>
                </div>
            </div>
            <button
                onClick={onClose}
                className="text-white/80 hover:text-white hover:bg-white/10 p-1 rounded-full transition-colors"
            >
                <X size={20} />
            </button>
        </div>
    );
};

export default ChatHeader;
