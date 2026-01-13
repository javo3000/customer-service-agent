import React from 'react';
import ReactMarkdown from 'react-markdown';
import { User, Bot, FileText } from 'lucide-react';
import { motion } from 'framer-motion';

const ChatBubble = ({ message, isUser }) => {
    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className={`flex w-full mb-6 ${isUser ? 'justify-end' : 'justify-start'}`}
        >
            <div className={`flex max-w-[80%] ${isUser ? 'flex-row-reverse' : 'flex-row'} gap-3`}>
                {/* Avatar */}
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${isUser ? 'bg-secondary text-white' : 'bg-primary text-white'
                    }`}>
                    {isUser ? <User size={18} /> : <Bot size={18} />}
                </div>

                {/* Message Content */}
                <div className={`p-4 rounded-2xl ${isUser
                        ? 'bg-secondary/10 border border-secondary/20 text-white rounded-tr-none'
                        : 'bg-dark-card border border-white/10 text-gray-200 rounded-tl-none shadow-lg'
                    }`}>
                    {isUser ? (
                        <p className="text-sm md:text-base">{message}</p>
                    ) : (
                        <div className="prose prose-invert prose-sm max-w-none">
                            <ReactMarkdown>{message}</ReactMarkdown>
                        </div>
                    )}
                </div>
            </div>
        </motion.div>
    );
};

export default ChatBubble;
