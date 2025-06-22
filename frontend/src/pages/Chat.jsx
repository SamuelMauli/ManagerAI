import { useTranslation } from 'react-i18next';
import { SendHorizontal, Bot } from 'lucide-react';

const Chat = () => {
  const { t } = useTranslation();

  return (
    <div className="flex h-[75vh] flex-col">
      {/* Cabeçalho da Página */}
      <div className="mb-8">
        <h1 className="text-4xl font-extrabold tracking-tight text-dark-text">
          {t('sidebar.chat')}
        </h1>
        <p className="mt-2 text-lg text-dark-text-secondary">
          {t('chat.subtitle')}
        </p>
      </div>

      {/* Interface do Chat */}
      <div className="flex flex-1 flex-col rounded-2xl border border-white/10 bg-dark-card/60 p-4 shadow-lg backdrop-blur-lg">
        {/* Área de Mensagens */}
        <div className="flex-1 space-y-4 overflow-y-auto p-4">
          {/* Mensagem da IA */}
          <div className="flex items-start gap-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-dark-accent">
              <Bot size={20} className="text-white" />
            </div>
            <div className="max-w-xs rounded-b-xl rounded-tr-xl bg-dark-primary p-3">
              <p className="text-sm text-dark-text">{t('chat.welcomeMessage')}</p>
            </div>
          </div>
        </div>

        {/* Área de Input */}
        <div className="mt-4 border-t border-white/10 pt-4">
          <div className="relative">
            <input
              type="text"
              placeholder={t('chat.inputPlaceholder')}
              className="w-full rounded-lg border border-transparent bg-dark-primary py-3 pl-4 pr-12 text-dark-text placeholder-dark-text-secondary focus:border-dark-accent focus:outline-none focus:ring-0"
            />
            <button className="absolute inset-y-0 right-0 flex items-center pr-4 text-dark-accent transition-transform hover:scale-110">
              <SendHorizontal size={20} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;