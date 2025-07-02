import React from 'react';
import { Bot, User } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

const Message = ({ role, content }) => {
  const isUser = role === 'user';
  
  const icon = isUser ? (
    <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-gray-600">
      <User size={20} className="text-white" />
    </div>
  ) : (
    <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-primary">
      <Bot size={20} className="text-primary-foreground" />
    </div>
  );

  return (
    <div className={`flex items-start gap-4 ${isUser ? 'justify-end' : ''}`}>
      {!isUser && icon}
      <div className={`max-w-xl rounded-b-xl p-3 shadow ${isUser ? 'rounded-tl-xl bg-blue-600 text-white' : 'rounded-tr-xl bg-muted'}`}>
        <div className="prose prose-sm dark:prose-invert max-w-none">
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      </div>
      {isUser && icon}
    </div>
  );
};

export default Message;