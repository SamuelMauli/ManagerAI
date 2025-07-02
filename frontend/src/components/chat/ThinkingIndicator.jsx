import React from 'react';
import { Bot, LoaderCircle } from 'lucide-react';

const ThinkingIndicator = ({ contextMessage }) => {
  return (
    <div className="flex items-start gap-4">
      <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-primary">
        <Bot size={20} className="text-primary-foreground" />
      </div>
      <div className="max-w-md rounded-b-xl rounded-tr-xl bg-muted p-3 shadow">
        <div className="flex items-center gap-2">
            <LoaderCircle size={20} className="animate-spin text-muted-foreground" />
            <p className="text-sm italic text-muted-foreground">
              {contextMessage || 'Assistant is thinking...'}
            </p>
        </div>
      </div>
    </div>
  );
};

export default ThinkingIndicator;