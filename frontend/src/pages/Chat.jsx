// frontend/src/pages/Chat.jsx
import React, { useState, useRef, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { toast } from 'react-hot-toast';
// ATUALIZE A IMPORTAÇÃO
import { chat } from '../services/api'; 

import Message from '../components/chat/Message';
import ChatInput from '../components/chat/ChatInput';
import ThinkingIndicator from '../components/chat/ThinkingIndicator';

const Chat = () => {
  const { t } = useTranslation();
  const [messages, setMessages] = useState([{ role: 'ai', content: t('chat.welcomeMessage') }]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSendMessage = async (input) => {
    if (!input.trim() || isLoading) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // ## LÓGICA ATUALIZADA ##
      // Prepara o histórico para enviar como contexto (opcional, mas bom para o futuro)
      const history = messages.slice(-10); // Envia as últimas 10 mensagens
      
      // Usa o novo serviço de chat
      const response = await chat.sendMessage(input, history);
      
      const aiMessage = response.data; // A resposta já vem no formato { role, content }
      setMessages(prev => [...prev, aiMessage]);

    } catch (error) {
      console.error("Falha ao obter resposta do chat:", error);
      const errorMessageContent = error.response?.data?.detail || t('chat.errors.response');
      toast.error(errorMessageContent);
      const errorMessage = { role: 'ai', content: errorMessageContent };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // O resto do seu JSX continua exatamente o mesmo...
  return (
    <div className="p-4 sm:p-6 flex h-full flex-col">
      {/* ... seu JSX aqui ... */}
      <div className="flex flex-1 flex-col rounded-2xl border bg-card/60 shadow-lg backdrop-blur-lg">
        <div className="flex-1 space-y-6 overflow-y-auto p-4">
          {messages.map((msg, index) => (
            <Message key={index} role={msg.role} content={msg.content} />
          ))}
          {isLoading && <ThinkingIndicator />}
          <div ref={messagesEndRef} />
        </div>
        <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
};

export default Chat;