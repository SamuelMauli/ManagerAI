import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { SendHorizontal } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

const ChatInput = ({ onSendMessage, isLoading }) => {
  const { t } = useTranslation();
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSendMessage(input);
    setInput('');
  };

  return (
    <form onSubmit={handleSubmit} className="mt-4 border-t p-4">
      <div className="relative">
        <Input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={t('chat.inputPlaceholder')}
          className="py-3 pl-4 pr-12"
          disabled={isLoading}
        />
        <Button 
          type="submit" 
          size="icon"
          className="absolute inset-y-0 right-0 mr-1.5 my-auto h-8 w-10"
          disabled={isLoading || !input.trim()}
        >
          <SendHorizontal size={20} />
        </Button>
      </div>
    </form>
  );
};

export default ChatInput;