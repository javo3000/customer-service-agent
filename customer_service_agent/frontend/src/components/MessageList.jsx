import React, { useRef, useEffect } from 'react';
import MessageBubble from './MessageBubble';

const MessageList = ({ messages = [] }) => {
    const bottomRef = useRef(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    return (
        <div className="flex-1 overflow-y-auto overflow-x-hidden p-4 space-y-4 bg-dark-bg scrollbar-hide">
            {messages.length === 0 && (
                <div className="text-center text-dark-muted mt-10 text-sm">
                    Start a conversation with AlFin!
                </div>
            )}

            {messages.map((msg, index) => (
                <MessageBubble key={index} message={msg} />
            ))}
            <div ref={bottomRef} />
        </div>
    );
};

export default MessageList;
