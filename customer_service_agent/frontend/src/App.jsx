import React from 'react';
import ChatWidget from './components/ChatWidget';
import HeroSection from './components/HeroSection';
import "./index.css"

function App() {
  return (
    <div className="min-h-screen bg-dark-bg text-white font-sans selection:bg-primary/30 relative overflow-hidden">
      {/* Background Gradients */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-primary/20 rounded-full blur-[120px]" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-secondary/10 rounded-full blur-[120px]" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto min-h-screen flex flex-col">
        {/* Main Content / Landing Page */}
        <div className="flex-1 flex flex-col justify-center items-center pb-32">
          <HeroSection />
          <div className="mt-12 text-center max-w-2xl px-4">
            <h2 className="text-2xl font-semibold mb-4 text-primary">Welcome to WorkMerate Support</h2>
            <p className="text-dark-muted">
              Click the chat icon in the bottom right corner to start a conversation with our AI agent.
            </p>
          </div>
        </div>

        {/* Chat Widget */}
        <ChatWidget />
      </div>
    </div>
  );
}

export default App;
