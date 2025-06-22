import { Dialog, Transition, Menu } from '@headlessui/react';
import { Fragment, useState } from 'react'; // 1. Importar useState
import { useUI } from '../../context/UIContext';
import { useTranslation } from 'react-i18next';
// 2. Importar novos ícones
import { X, Languages, Check, RefreshCw, KeyRound, Mail } from 'lucide-react'; 

const supportedLanguages = [
  // ... (array de idiomas continua o mesmo)
  { code: 'en', name: 'English' },
  { code: 'pt', name: 'Português' },
  { code: 'es', name: 'Español' },
  { code: 'de', name: 'Deutsch' },
];

export default function SettingsModal() {
  const { isSettingsModalOpen, closeSettingsModal } = useUI();
  const { t, i18n } = useTranslation();

  // 3. Estados para os campos de input de email
  const [email, setEmail] = useState('');
  const [credentials, setCredentials] = useState('');

  const currentLanguage = supportedLanguages.find(lang => lang.code === i18n.language);
  
  // Funções de placeholder para os cliques dos botões
  const handleYoutrackJob = () => alert('Rodando job do YouTrack...');
  const handleEmailJob = () => alert(`Atualizando emails para: ${email}`);


  return (
    <Transition appear show={isSettingsModalOpen} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={closeSettingsModal}>
        {/* ... (Backdrop e container do Dialog continuam os mesmos) ... */}
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm" />
        </Transition.Child>

        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4 text-center">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <Dialog.Panel className="w-full max-w-md transform divide-y divide-white/10 rounded-2xl border border-white/10 bg-light-primary p-6 text-left align-middle shadow-2xl transition-all dark:bg-dark-primary">
                {/* Seção do Título */}
                <div className="pb-4">
                    <Dialog.Title
                      as="h3"
                      className="text-lg font-medium leading-6 text-light-text dark:text-dark-text"
                    >
                      {t('sidebar.settings')}
                    </Dialog.Title>
                </div>

                {/* === INÍCIO DAS NOVAS SEÇÕES DE JOBS === */}
                <div className="py-4">
                  <h4 className="mb-2 text-sm font-semibold text-light-text dark:text-dark-text">
                    {t('jobs.youtrackTitle')}
                  </h4>
                  <p className="mb-4 text-sm text-light-text-secondary dark:text-dark-text-secondary">
                    {t('jobs.youtrackDescription')}
                  </p>
                  <button 
                    onClick={handleYoutrackJob}
                    className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-dark-accent/80 px-4 py-2 font-semibold text-white transition-colors hover:bg-dark-accent"
                  >
                    <RefreshCw size={16} />
                    {t('jobs.youtrackButton')}
                  </button>
                </div>

                <div className="py-4">
                  <h4 className="mb-2 text-sm font-semibold text-light-text dark:text-dark-text">
                    {t('jobs.emailTitle')}
                  </h4>
                   <p className="mb-4 text-sm text-light-text-secondary dark:text-dark-text-secondary">
                    {t('jobs.emailDescription')}
                  </p>
                  <div className="space-y-4">
                    <div className="relative">
                      <Mail size={16} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-dark-text-secondary" />
                      <input 
                        type="email"
                        placeholder={t('jobs.emailAddressPlaceholder')}
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="w-full rounded-md border border-white/20 bg-dark-background py-2 pl-10 pr-4 text-sm text-dark-text focus:border-dark-accent focus:ring-dark-accent"
                      />
                    </div>
                     <div className="relative">
                      <KeyRound size={16} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-dark-text-secondary" />
                      <input 
                        type="password"
                        placeholder={t('jobs.emailCredentialsPlaceholder')}
                        value={credentials}
                        onChange={(e) => setCredentials(e.target.value)}
                        className="w-full rounded-md border border-white/20 bg-dark-background py-2 pl-10 pr-4 text-sm text-dark-text focus:border-dark-accent focus:ring-dark-accent"
                      />
                    </div>
                     <button 
                        onClick={handleEmailJob}
                        className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-dark-accent/80 px-4 py-2 font-semibold text-white transition-colors hover:bg-dark-accent"
                     >
                        <RefreshCw size={16} />
                        {t('jobs.emailUpdateButton')}
                    </button>
                  </div>
                </div>
                {/* === FIM DAS NOVAS SEÇÕES DE JOBS === */}
                
                {/* Seção de Idioma (existente) */}
                <div className="pt-4">
                  <h4 className="mb-2 text-sm font-semibold text-light-text dark:text-dark-text">
                    {t('settings.languageTitle')}
                  </h4>
                  <Menu as="div" className="relative inline-block w-full text-left">
                    {/* ... (Dropdown de idiomas continua o mesmo) ... */}
                    <div>
                      <Menu.Button className="inline-flex w-full justify-between rounded-md border border-white/20 bg-dark-background px-4 py-2 text-sm font-medium text-dark-text hover:bg-dark-primary focus:outline-none focus-visible:ring-2 focus-visible:ring-dark-accent focus-visible:ring-opacity-75">
                        {currentLanguage?.name || t('settings.languagePlaceholder')}
                        <Languages
                          className="ml-2 -mr-1 h-5 w-5 text-dark-text-secondary"
                          aria-hidden="true"
                        />
                      </Menu.Button>
                    </div>
                    <Transition
                      as={Fragment}
                      enter="transition ease-out duration-100"
                      enterFrom="transform opacity-0 scale-95"
                      enterTo="transform opacity-100 scale-100"
                      leave="transition ease-in duration-75"
                      leaveFrom="transform opacity-100 scale-100"
                      leaveTo="transform opacity-0 scale-95"
                    >
                      <Menu.Items className="absolute right-0 z-10 mt-2 w-full origin-top-right divide-y divide-gray-100/10 rounded-md bg-dark-primary shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                        <div className="px-1 py-1 ">
                          {supportedLanguages.map((lang) => (
                            <Menu.Item key={lang.code}>
                              {({ active }) => (
                                <button
                                  onClick={() => i18n.changeLanguage(lang.code)}
                                  className={`${
                                    active ? 'bg-dark-accent text-white' : 'text-dark-text'
                                  } group flex w-full items-center rounded-md px-2 py-2 text-sm`}
                                >
                                  {i18n.language === lang.code ? (
                                    <Check className="mr-2 h-5 w-5" />
                                  ) : (
                                    <span className="mr-2 h-5 w-5" />
                                  )}
                                  {lang.name}
                                </button>
                              )}
                            </Menu.Item>
                          ))}
                        </div>
                      </Menu.Items>
                    </Transition>
                  </Menu>
                </div>
                
                <button
                  onClick={closeSettingsModal}
                  className="absolute top-3 right-3 rounded-full p-2 text-light-text-secondary transition-colors hover:bg-black/20 hover:text-white dark:text-dark-text-secondary"
                  aria-label="Fechar modal"
                >
                  <X size={20} />
                </button>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition>
  );
}