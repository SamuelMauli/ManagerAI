import React, { useState, useRef, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { toast } from 'react-hot-toast';
import api from '../services/api'; // Certifique-se que o caminho está correto

import Message from '../components/chat/Message';
import ChatInput from '../components/chat/ChatInput';
import ThinkingIndicator from '../components/chat/ThinkingIndicator';

const Chat = () => {
  const { t } = useTranslation();
  const [messages, setMessages] = useState([{ role: 'ai', content: t('chat.welcomeMessage') }]);
  const [isLoading, setIsLoading] = useState(false);
  const [contextMessage, setContextMessage] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages, isLoading]);

  const handleSendMessage = async (input) => {
    if (!input.trim() || isLoading) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setContextMessage(t('chat.contextMessage')); // Mostra a mensagem de contexto

    try {
      // A API agora usa o serviço de IA contextual (RAG)
      const response = await api.postChatMessage(input);
      const aiMessage = { role: 'ai', content: response.data }; // Ajuste conforme a resposta da sua API
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error("Failed to get chat response:", error);
      toast.error(t('chat.errors.response'));
      const errorMessage = { role: 'ai', content: t('chat.errors.response') };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setContextMessage(''); // Limpa a mensagem de contexto
    }
  };

  return (
    <div className="p-4 sm:p-6 flex h-full flex-col">
      <div className="mb-6">
        <h1 className="text-4xl font-extrabold tracking-tight">
          {t('sidebar.chat')}
        </h1>
        <p className="mt-2 text-lg text-muted-foreground">
          {t('chat.subtitle')}
        </p>
      </div>

      <div className="flex flex-1 flex-col rounded-2xl border bg-card/60 shadow-lg backdrop-blur-lg">
        <div className="flex-1 space-y-6 overflow-y-auto p-4">
          {messages.map((msg, index) => (
            <Message key={index} role={msg.role} content={msg.content} />
          ))}
          {isLoading && <ThinkingIndicator contextMessage={contextMessage} />}
          <div ref={messagesEndRef} />
        </div>
        <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
};

export default Chat;