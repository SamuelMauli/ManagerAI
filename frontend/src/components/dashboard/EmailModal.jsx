import React from 'react';
import { X } from 'lucide-react';

const EmailModal = ({ emails, onClose }) => {
  const formatDateTime = (dateTime) => new Date(dateTime).toLocaleString('pt-BR', {
    dateStyle: 'short',
    timeStyle: 'short'
  });

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
      onClick={onClose}
    >
      <div 
        className="bg-card text-card-foreground w-11/12 max-w-2xl rounded-lg shadow-xl relative max-h-[90vh] flex flex-col"
        onClick={e => e.stopPropagation()} 
      >
        <div className="p-6 border-b">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-semibold tracking-tight">E-mails não Lidos</h2>
            <button 
              onClick={onClose} 
              className="p-1 rounded-full hover:bg-muted"
            >
              <X className="h-6 w-6" />
            </button>
          </div>
        </div>

        <div className="p-6 overflow-y-auto">
          <ul className="space-y-4">
            {emails.map(email => (
              <li key={email.google_email_id} className="border-b pb-4 last:border-b-0">
                <div className="flex justify-between items-start">
                  <p className="font-semibold text-base pr-4">{email.subject || '(Sem assunto)'}</p>
                  <span className="text-xs text-muted-foreground whitespace-nowrap">{formatDateTime(email.received_at)}</span>
                </div>
                <p className="text-sm text-muted-foreground mt-1">De: {email.sender}</p>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default EmailModal;