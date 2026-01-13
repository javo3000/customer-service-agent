import React, { useState } from 'react';
import { MessageCircle, X } from 'lucide-react';
import { AnimatePresence, motion } from 'framer-motion';
import ChatHeader from './ChatHeader';
import MessageList from './MessageList';
import ChatInput from './ChatInput';
import { askAgent } from '../api';

const ChatWidget = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isThinking, setIsThinking] = useState(false);

    const toggleChat = () => setIsOpen(!isOpen);

    const handleSend = async (question) => {
        const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const assistantMessageId = Date.now() + 1; // Unique ID

        const userMessage = {
            role: 'user',
            content: question,
            timestamp
        };

        const initialAssistantMessage = {
            id: assistantMessageId,
            role: 'assistant',
            content: '',
            timestamp,
            isThinking: true
        };

        // Batch these two so the assistant message is guaranteed to exist before streaming starts
        setMessages(prev => [...prev, userMessage, initialAssistantMessage]);
        setIsLoading(true);
        setIsThinking(true);

        let fullContent = '';
        let metadata = null;

        try {
            const chatHistory = messages.map(msg => ({
                role: msg.role,
                content: msg.content
            }));

            await askAgent(question, chatHistory, (chunk) => {
                if (chunk.type === 'token') {
                    setIsThinking(false);
                    fullContent += chunk.content;
                    setMessages(prev => prev.map(msg =>
                        msg.id === assistantMessageId
                            ? { ...msg, content: fullContent, isThinking: false }
                            : msg
                    ));
                } else if (chunk.type === 'metadata') {
                    metadata = chunk.content;
                    setMessages(prev => prev.map(msg =>
                        msg.id === assistantMessageId
                            ? { ...msg, route: metadata.route, sources: metadata.needed_sources }
                            : msg
                    ));
                } else if (chunk.type === 'thinking') {
                    setIsThinking(chunk.content);
                    setMessages(prev => prev.map(msg =>
                        msg.id === assistantMessageId
                            ? { ...msg, isThinking: chunk.content }
                            : msg
                    ));
                } else if (chunk.type === 'status') {
                    console.log("Stream Status:", chunk.content);
                }
            });

        } catch (error) {
            console.error("Error sending message:", error);
            setMessages(prev => prev.map(msg =>
                msg.id === assistantMessageId
                    ? { ...msg, content: "I apologize, but I encountered an error processing your request. Please try again later.", isThinking: false }
                    : msg
            ));
        } finally {
            setIsLoading(false);
            setIsThinking(false);
        }
    };

    return (
        <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end font-sans">
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: 20, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 20, scale: 0.95 }}
                        transition={{ duration: 0.2 }}
                        className="mb-4 w-[380px] h-[600px] bg-dark-bg rounded-2xl shadow-2xl overflow-hidden flex flex-col border border-dark-border"
                    >
                        <ChatHeader onClose={toggleChat} />
                        <MessageList messages={messages} />
                        <ChatInput onSend={handleSend} isLoading={isLoading} />
                    </motion.div>
                )}
            </AnimatePresence>

            <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={toggleChat}
                className="bg-primary hover:bg-primary-dark text-white p-4 rounded-full shadow-lg flex items-center justify-center transition-colors"
            >
                {isOpen ? <X size={24} /> : <MessageCircle size={24} />}
            </motion.button>
        </div>
    );
};

export default ChatWidget;
