import React from 'react';
import { Bot, ThumbsUp, ThumbsDown, User } from 'lucide-react';
import { motion } from 'framer-motion';
import { cn } from '../utils';

const MessageBubble = ({ message }) => {
    const isBot = message.role === 'assistant';

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={cn(
                "flex gap-3 max-w-[90%]",
                isBot ? "self-start" : "self-end flex-row-reverse"
            )}
        >
            <div className={cn(
                "w-8 h-8 rounded-full flex items-center justify-center shrink-0",
                isBot ? "bg-primary" : "bg-secondary"
            )}>
                {isBot ? <Bot size={16} className="text-white" /> : <User size={16} className="text-white" />}
            </div>

            <div className="flex flex-col gap-1 min-w-0">
                <div className={cn(
                    "p-3 rounded-2xl text-sm shadow-sm",
                    isBot
                        ? "bg-dark-card text-dark-text rounded-tl-none border border-dark-border"
                        : "bg-primary/10 text-dark-text rounded-tr-none border border-primary/20"
                )}>
                    <p className="whitespace-pre-wrap break-words leading-relaxed">{message.content}</p>
                </div>

                <div className={cn(
                    "flex items-center gap-2 text-[10px] text-dark-muted",
                    isBot ? "justify-start" : "justify-end"
                )}>
                    <span>{message.timestamp || 'Just now'}</span>
                    {isBot && (
                        <div className="flex gap-1 ml-2">
                            <button className="hover:text-primary transition-colors"><ThumbsUp size={12} /></button>
                            <button className="hover:text-secondary transition-colors"><ThumbsDown size={12} /></button>
                        </div>
                    )}
                </div>
            </div>
        </motion.div>
    );
};

export default MessageBubble;
