import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { SendHorizontal, Bot, User, LoaderCircle } from 'lucide-react';
import { postChatMessage } from '../services/api';

const Chat = () => {
  const { t } = useTranslation();
  const [messages, setMessages] = useState([
    { role: 'ai', content: t('chat.welcomeMessage') }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await postChatMessage(input);
      const aiMessage = { role: 'ai', content: response.data.message };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      const errorMessage = { role: 'ai', content: 'Sorry, I had trouble responding. Please try again.' };
      setMessages(prev => [...prev, errorMessage]);
      console.error("Failed to get chat response:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-[80vh] flex-col">
      <div className="mb-6">
        <h1 className="text-4xl font-extrabold tracking-tight text-dark-text">
          {t('sidebar.chat')}
        </h1>
        <p className="mt-2 text-lg text-dark-text-secondary">
          {t('chat.subtitle')}
        </p>
      </div>

      <div className="flex flex-1 flex-col rounded-2xl border border-white/10 bg-dark-card/60 p-4 shadow-lg backdrop-blur-lg">
        <div className="flex-1 space-y-6 overflow-y-auto p-4">
          {messages.map((msg, index) => (
            <div key={index} className={`flex items-start gap-4 ${msg.role === 'user' ? 'justify-end' : ''}`}>
              {msg.role === 'ai' && (
                <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-dark-accent">
                  <Bot size={20} className="text-white" />
                </div>
              )}
              <div className={`max-w-md rounded-b-xl p-3 ${msg.role === 'user' ? 'rounded-tl-xl bg-blue-600' : 'rounded-tr-xl bg-dark-primary'}`}>
                <p className="text-sm text-dark-text">{msg.content}</p>
              </div>
               {msg.role === 'user' && (
                <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-gray-600">
                  <User size={20} className="text-white" />
                </div>
              )}
            </div>
          ))}
          {isLoading && (
             <div className="flex items-start gap-3">
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-dark-accent">
                    <LoaderCircle size={20} className="text-white animate-spin" />
                </div>
                <div className="max-w-xs rounded-b-xl rounded-tr-xl bg-dark-primary p-3">
                    <p className="text-sm text-dark-text-secondary italic">Assistant is typing...</p>
                </div>
            </div>
          )}
        </div>

        <form onSubmit={handleSendMessage} className="mt-4 border-t border-white/10 pt-4">
          <div className="relative">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={t('chat.inputPlaceholder')}
              className="w-full rounded-lg border border-transparent bg-dark-primary py-3 pl-4 pr-12 text-dark-text placeholder-dark-text-secondary focus:border-dark-accent focus:outline-none focus:ring-0"
              disabled={isLoading}
            />
            <button type="submit" className="absolute inset-y-0 right-0 flex items-center pr-4 text-dark-accent transition-transform hover:scale-110 disabled:opacity-50" disabled={isLoading}>
              <SendHorizontal size={20} />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Chat;