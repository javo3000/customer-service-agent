import React from 'react';
import { motion } from 'framer-motion';
import { Sparkles } from 'lucide-react';

const HeroSection = () => {
    return (
        <div className="text-center py-12 px-4">
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-sm font-medium mb-6"
            >
                <Sparkles size={14} />
                <span>AI-Powered Tax Advisory</span>
            </motion.div>

            <motion.h1
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.1 }}
                className="text-4xl md:text-6xl font-bold text-primary mb-6 tracking-tight"
            >
                Intelligent Support <br />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-light via-primary to-secondary">
                    For Your Business
                </span>
            </motion.h1>

            <motion.p
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
                className="text-gray-400 text-lg max-w-2xl mx-auto mb-8"
            >
                Experience the future of customer service. Ask about your orders,
                legal policies, or general inquiries with our advanced AI agent.
            </motion.p>
        </div>
    );
};

export default HeroSection;
