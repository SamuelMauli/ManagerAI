import { Dialog, Transition, Menu } from '@headlessui/react';
import { Fragment, useState, useEffect } from 'react';
import { useUI } from '../../context/UIContext';
import { useTranslation } from 'react-i18next';
import api from '../../services/api';
import { X, Languages, Check, RefreshCw, KeyRound, Mail, Save } from 'lucide-react'; 

const supportedLanguages = [
  { code: 'en', name: 'English' },
  { code: 'pt', name: 'Português' },
  { code: 'es', name: 'Español' },
  { code: 'de', name: 'Deutsch' },
];

export default function SettingsModal() {
  const { isSettingsModalOpen, closeSettingsModal } = useUI();
  const { t, i18n } = useTranslation();

  const [youtrackUrl, setYoutrackUrl] = useState('');
  const [youtrackToken, setYoutrackToken] = useState('');

  const [emailAddress, setEmailAddress] = useState('');
  const [emailPassword, setEmailPassword] = useState(''); 
  const currentLanguage = supportedLanguages.find(lang => lang.code === i18n.language);
  
  useEffect(() => {
    if (isSettingsModalOpen) {
      api.get('/settings/youtrack')
        .then(response => {
          if (response.data) {
            setYoutrackUrl(response.data.base_url || '');
          }
        })
        .catch(error => console.error('Could not load YouTrack settings.', error));
      
      api.get('/settings/gmail')
        .then(response => {
            if(response.data) {
                setEmailAddress(response.data.email || '');
            }
        })
        .catch(error => console.error('Could not load Email settings.', error));
    }
  }, [isSettingsModalOpen]);

  // --- Handler Functions ---

  // Saves YouTrack settings
  const handleSaveYoutrack = async () => {
    try {
      await api.post('/settings/youtrack', { base_url: youtrackUrl, token: youtrackToken });
      alert(t('settings.youtrackSaveSuccess'));
      setYoutrackToken(''); // Clear the token field after saving
    } catch (error) {
      console.error('Failed to save YouTrack settings', error);
      alert(t('settings.youtrackSaveError'));
    }
  };

  // Saves Email settings
  const handleSaveEmail = async () => {
    try {
        await api.post('/settings/gmail', { email: emailAddress, password: emailPassword });
        alert(t('settings.emailSaveSuccess'));
        setEmailPassword(''); // Clear the password field after saving
    } catch (error) {
        console.error('Failed to save Email settings', error);
        alert(t('settings.emailSaveError'));
    }
  };

  // Triggers the YouTrack sync job
  const handleRunYoutrackJob = async () => {
    try {
        await api.post('/jobs/youtrack/sync');
        alert(t('jobs.youtrackJobSuccess'));
    } catch (error) {
        console.error('Failed to run YouTrack job', error);
        alert(t('jobs.youtrackJobError'));
    }
  };

  // Triggers the Email sync job
  const handleRunEmailJob = async () => {
    try {
        await api.post('/jobs/email/sync');
        alert(t('jobs.emailJobSuccess'));
    } catch (error) {
        console.error('Failed to run Email job', error);
        alert(t('jobs.emailJobError'));
    }
  };


  return (
    <Transition appear show={isSettingsModalOpen} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={closeSettingsModal}>
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
                
                <div className="pb-4 flex justify-between items-center">
                    <Dialog.Title as="h3" className="text-lg font-medium leading-6 text-light-text dark:text-dark-text">
                      {t('sidebar.settings')}
                    </Dialog.Title>
                    <button
                        onClick={closeSettingsModal}
                        className="rounded-full p-2 text-light-text-secondary transition-colors hover:bg-black/20 hover:text-white dark:text-dark-text-secondary"
                        aria-label={t('settings.closeModal')}
                    >
                        <X size={20} />
                    </button>
                </div>

                {/* === YouTrack Settings Section === */}
                <div className="py-4">
                  <h4 className="mb-2 text-md font-semibold text-light-text dark:text-dark-text">
                    {t('settings.youtrackTitle')}
                  </h4>
                  <div className="space-y-4">
                    {/* YouTrack URL Input */}
                    <div className="relative">
                       <input 
                        type="text"
                        placeholder={t('settings.youtrackUrlPlaceholder')}
                        value={youtrackUrl}
                        onChange={(e) => setYoutrackUrl(e.target.value)}
                        className="w-full rounded-md border border-white/20 bg-dark-background py-2 px-4 text-sm text-dark-text focus:border-dark-accent focus:ring-dark-accent"
                      />
                    </div>
                    {/* YouTrack Token Input */}
                     <div className="relative">
                      <KeyRound size={16} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-dark-text-secondary" />
                      <input 
                        type="password"
                        placeholder={t('settings.youtrackTokenPlaceholder')}
                        value={youtrackToken}
                        onChange={(e) => setYoutrackToken(e.target.value)}
                        className="w-full rounded-md border border-white/20 bg-dark-background py-2 pl-10 pr-4 text-sm text-dark-text focus:border-dark-accent focus:ring-dark-accent"
                      />
                    </div>
                     <button 
                        onClick={handleSaveYoutrack}
                        className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600/80 px-4 py-2 font-semibold text-white transition-colors hover:bg-blue-600"
                     >
                        <Save size={16} />
                        {t('settings.saveButton')}
                    </button>
                    <button 
                        onClick={handleRunYoutrackJob}
                        className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-dark-accent/80 px-4 py-2 font-semibold text-white transition-colors hover:bg-dark-accent"
                    >
                        <RefreshCw size={16} />
                        {t('jobs.youtrackButton')}
                    </button>
                  </div>
                </div>

                {/* === Gmail Settings Section === */}
                <div className="py-4">
                   <h4 className="mb-2 text-md font-semibold text-light-text dark:text-dark-text">
                    {t('settings.emailTitle')}
                  </h4>
                   <p className="mb-4 text-sm text-light-text-secondary dark:text-dark-text-secondary">
                    {t('settings.emailDescription')}
                  </p>
                  <div className="space-y-4">
                    {/* Email Address Input */}
                    <div className="relative">
                      <Mail size={16} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-dark-text-secondary" />
                      <input 
                        type="email"
                        placeholder={t('settings.emailAddressPlaceholder')}
                        value={emailAddress}
                        onChange={(e) => setEmailAddress(e.target.value)}
                        className="w-full rounded-md border border-white/20 bg-dark-background py-2 pl-10 pr-4 text-sm text-dark-text focus:border-dark-accent focus:ring-dark-accent"
                      />
                    </div>
                    {/* Email App Password Input */}
                     <div className="relative">
                      <KeyRound size={16} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-dark-text-secondary" />
                      <input 
                        type="password"
                        placeholder={t('settings.emailCredentialsPlaceholder')}
                        value={emailPassword}
                        onChange={(e) => setEmailPassword(e.target.value)}
                        className="w-full rounded-md border border-white/20 bg-dark-background py-2 pl-10 pr-4 text-sm text-dark-text focus:border-dark-accent focus:ring-dark-accent"
                      />
                    </div>
                     <button 
                        onClick={handleSaveEmail}
                        className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600/80 px-4 py-2 font-semibold text-white transition-colors hover:bg-blue-600"
                     >
                        <Save size={16} />
                        {t('settings.saveButton')}
                    </button>
                    <button 
                        onClick={handleRunEmailJob}
                        className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-dark-accent/80 px-4 py-2 font-semibold text-white transition-colors hover:bg-dark-accent"
                    >
                        <RefreshCw size={16} />
                        {t('jobs.emailUpdateButton')}
                    </button>
                  </div>
                </div>
                
                {/* === Language Settings Section === */}
                <div className="pt-4">
                  <h4 className="mb-2 text-md font-semibold text-light-text dark:text-dark-text">
                    {t('settings.languageTitle')}
                  </h4>
                  <Menu as="div" className="relative inline-block w-full text-left">
                    <div>
                      <Menu.Button className="inline-flex w-full justify-between rounded-md border border-white/20 bg-dark-background px-4 py-2 text-sm font-medium text-dark-text hover:bg-dark-primary focus:outline-none focus-visible:ring-2 focus-visible:ring-dark-accent focus-visible:ring-opacity-75">
                        {currentLanguage?.name || t('settings.languagePlaceholder')}
                        <Languages className="ml-2 -mr-1 h-5 w-5 text-dark-text-secondary" aria-hidden="true"/>
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
                      <Menu.Items className="absolute bottom-full mb-2 w-full origin-bottom-right divide-y divide-gray-100/10 rounded-md bg-dark-primary shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
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
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition>
  );
}