import { Dialog, Transition, Menu, Listbox } from '@headlessui/react'; // Adicionado Listbox
import { Fragment, useState, useEffect } from 'react';
import { useUI } from '../../context/UIContext';
import { useTranslation } from 'react-i18next';
import toast from 'react-hot-toast';
import api from '../../services/api';
import { X, Languages, Check, RefreshCw, Save, LoaderCircle } from 'lucide-react';

// Seus componentes ShadCN que você quer manter:
import { Button } from './button';
import { Input } from './input';
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from './card';
// Remova esta linha se você não a usa mais para outros Label no modal, ou adapte para uma label simples HTML:
// import { Label } from './label'; 

const supportedLanguages = [
  { code: 'en', name: 'English' },
  { code: 'pt', name: 'Português' },
  { code: 'es', name: 'Español' },
  { code: 'de', name: 'Deutsch' },
];

export default function SettingsModal() {
  const { isSettingsModalOpen, closeSettingsModal } = useUI();
  const { t, i18n } = useTranslation();

  // State for YouTrack and Email settings
  const [youTrackUrl, setYouTrackUrl] = useState('');
  const [youTrackToken, setYouTrackToken] = useState('');
  const [emailAddress, setEmailAddress] = useState('');
  const [emailPassword, setEmailPassword] = useState('');

  // UI state for loading indicators
  const [isLoading, setIsLoading] = useState(false);
  const [isSavingYouTrack, setIsSavingYouTrack] = useState(false);
  const [isSavingEmail, setIsSavingEmail] = useState(false);
  const [isSyncingYouTrack, setIsSyncingYouTrack] = useState(false);
  const [isSyncingEmail, setIsSyncingEmail] = useState(false);

  // Estado para o idioma (mantido para o Listbox)
  const [currentLanguage, setCurrentLanguage] = useState(i18n.language);

  // Funções dummy para simular chamadas de API (substitua pelas suas reais do api.js)
  // Certifique-se de que estas funções existem e estão exportadas em `api.js`
  const getYouTrackSettings = async () => api.getSettings(); // Ou a rota específica
  const getEmailSettings = async () => api.getSettings(); // Ou a rota específica
  const saveYouTrackSettings = async (data) => api.saveSettings(data);
  const saveEmailSettings = async (data) => api.saveSettings(data);
  const runYouTrackJob = async () => api.runYoutrackJob();
  const runEmailJob = async () => api.syncEmails();


  useEffect(() => {
    if (isSettingsModalOpen) {
      const loadAllSettings = async () => {
        setIsLoading(true);
        try {
          const res = await api.getSettings(); // Supondo que `getSettings` traga todas as configurações
          const settings = res.data;

          setYouTrackUrl(settings.youtrack_base_url || '');
          setYouTrackToken(settings.youtrack_api_token || '');
          setEmailAddress(settings.google_email || '');
          // Não carregamos a senha por segurança, apenas o e-mail
          // setEmailPassword(settings.google_app_password || ''); 
        } catch (error) {
          console.error('Could not load settings.', error);
          toast.error(t('settings.errors.load') || 'Falha ao carregar configurações.');
        } finally {
          setIsLoading(false);
        }
      };
      loadAllSettings();
    }
  }, [isSettingsModalOpen, t]);

  const handleSaveYouTrack = async () => {
    setIsSavingYouTrack(true);
    const promise = saveYouTrackSettings({ youtrack_base_url: youTrackUrl, youtrack_api_token: youTrackToken });
    
    toast.promise(promise, {
      loading: t('settings.savingYouTrack'),
      success: t('settings.successYouTrack'),
      error: t('settings.errors.saveYouTrack'),
    }).finally(() => setIsSavingYouTrack(false));
  };

  const handleRunYouTrackJob = async () => {
    setIsSyncingYouTrack(true);
    const promise = runYouTrackJob();

    toast.promise(promise, {
      loading: t('jobs.syncing'),
      success: t('jobs.youtrackJobSuccess'), // Corrigido para a chave correta de jobs
      error: t('jobs.youtrackJobError'),    // Corrigido para a chave correta de jobs
    }).finally(() => setIsSyncingYouTrack(false));
  };

  const handleSaveEmail = async () => {
    setIsSavingEmail(true);
    const promise = saveEmailSettings({ google_email: emailAddress, google_app_password: emailPassword });
    
    toast.promise(promise, {
      loading: t('settings.savingEmail'),
      success: t('settings.successEmail'),
      error: t('settings.errors.saveEmail'),
    }).finally(() => {
      setEmailPassword(''); // Limpa a senha após salvar por segurança
      setIsSavingEmail(false);
    });
  };

  const handleRunEmailJob = async () => {
    setIsSyncingEmail(true);
    const promise = runEmailJob();

    toast.promise(promise, {
      loading: t('jobs.syncing'),
      success: t('jobs.emailJobSuccess'), // Corrigido para a chave correta de jobs
      error: t('jobs.emailJobError'),    // Corrigido para a chave correta de jobs
    }).finally(() => setIsSyncingEmail(false));
  };

  const handleLanguageChange = (lng) => {
    i18n.changeLanguage(lng);
    setCurrentLanguage(lng);
    toast.success(t('settings.languageChangeSuccess') || 'Idioma alterado com sucesso!');
  };

  return (
    <Transition appear show={isSettingsModalOpen} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={closeSettingsModal}>
        <Transition.Child as={Fragment} enter="ease-out duration-300" enterFrom="opacity-0" enterTo="opacity-100" leave="ease-in duration-200" leaveFrom="opacity-100" leaveTo="opacity-0">
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm" />
        </Transition.Child>

        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4 text-center">
            <Transition.Child as={Fragment} enter="ease-out duration-300" enterFrom="opacity-0 scale-95" enterTo="opacity-100 scale-100" leave="ease-in duration-200" leaveFrom="opacity-100 scale-100" leaveTo="opacity-0 scale-95">
              <Dialog.Panel className="w-full max-w-md transform divide-y divide-white/10 rounded-2xl border border-white/10 bg-dark-primary p-6 text-left align-middle shadow-2xl transition-all">
                
                <div className="pb-4 flex justify-between items-center">
                  <Dialog.Title as="h3" className="text-lg font-medium leading-6 text-dark-text">
                    {t('sidebar.settings')}
                  </Dialog.Title>
                  <button onClick={closeSettingsModal} className="rounded-full p-2 text-dark-text-secondary transition-colors hover:bg-black/20 hover:text-white" aria-label={t('settings.closeModal')}>
                    <X size={20} />
                  </button>
                </div>

                {isLoading ? (
                  <div className="flex justify-center items-center h-64">
                    <LoaderCircle size={32} className="animate-spin text-dark-accent" />
                  </div>
                ) : (
                  <>
                    <div className="py-4">
                      <h4 className="mb-2 text-md font-semibold text-dark-text">{t('settings.youtrackTitle')}</h4>
                      <div className="space-y-4">
                         <input type="text" placeholder="YouTrack URL" value={youTrackUrl} onChange={(e) => setYouTrackUrl(e.target.value)} className="w-full rounded-md border border-white/20 bg-dark-background py-2 px-4 text-sm text-dark-text focus:border-dark-accent focus:ring-dark-accent" />
                         <input type="password" placeholder="YouTrack Token" value={youTrackToken} onChange={(e) => setYouTrackToken(e.target.value)} className="w-full rounded-md border border-white/20 bg-dark-background py-2 px-4 text-sm text-dark-text focus:border-dark-accent focus:ring-dark-accent" />
                         <div className="flex gap-4">
                           <button onClick={handleSaveYouTrack} disabled={isSavingYouTrack} className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-2 font-semibold text-white transition-colors hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed">
                              {isSavingYouTrack ? <LoaderCircle size={16} className="animate-spin" /> : <Save size={16} />}
                              {t('settings.saveButton')}
                           </button>
                           <button onClick={handleRunYouTrackJob} disabled={isSyncingYouTrack} className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-dark-accent px-4 py-2 font-semibold text-white transition-colors hover:bg-dark-accent/80 disabled:opacity-50 disabled:cursor-not-allowed">
                              {isSyncingYouTrack ? <LoaderCircle size={16} className="animate-spin" /> : <RefreshCw size={16} />}
                              {t('jobs.youtrackButton')}
                           </button>
                         </div>
                      </div>
                    </div>

                    <div className="py-4">
                      <h4 className="mb-2 text-md font-semibold text-dark-text">{t('settings.emailTitle')}</h4>
                      <div className="space-y-4">
                        <input type="email" placeholder={t('settings.emailAddressPlaceholder')} value={emailAddress} onChange={(e) => setEmailAddress(e.target.value)} className="w-full rounded-md border border-white/20 bg-dark-background py-2 px-4 text-sm text-dark-text focus:border-dark-accent focus:ring-dark-accent" />
                        <input type="password" placeholder={t('settings.emailCredentialsPlaceholder')} value={emailPassword} onChange={(e) => setEmailPassword(e.target.value)} className="w-full rounded-md border border-white/20 bg-dark-background py-2 px-4 text-sm text-dark-text focus:border-dark-accent focus:ring-dark-accent" />
                        <div className="flex gap-4">
                          <button onClick={handleSaveEmail} disabled={isSavingEmail} className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-2 font-semibold text-white transition-colors hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed">
                             {isSavingEmail ? <LoaderCircle size={16} className="animate-spin" /> : <Save size={16} />}
                             {t('settings.saveButton')}
                          </button>
                          <button onClick={handleRunEmailJob} disabled={isSyncingEmail} className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-dark-accent px-4 py-2 font-semibold text-white transition-colors hover:bg-dark-accent/80 disabled:opacity-50 disabled:cursor-not-allowed">
                             {isSyncingEmail ? <LoaderCircle size={16} className="animate-spin" /> : <RefreshCw size={16} />}
                             {t('jobs.emailUpdateButton')}
                          </button>
                        </div>
                      </div>
                    </div>
                    
                    <div className="pt-4">
                      <h4 className="mb-2 text-md font-semibold text-dark-text">{t('settings.languageTitle')}</h4>
                      {/* Usando Listbox do Headless UI para seleção de idioma */}
                      <Listbox value={currentLanguage.code} onChange={handleLanguageChange}>
                        {({ open }) => (
                          <div className="relative mt-1">
                            <Listbox.Button className="relative w-full cursor-default rounded-md border border-white/20 bg-dark-background py-2 pl-3 pr-10 text-left text-dark-text shadow-sm focus:border-dark-accent focus:outline-none focus:ring-1 focus:ring-dark-accent sm:text-sm">
                              <span className="block truncate">{currentLanguage?.name || t('settings.languagePlaceholder')}</span>
                              <span className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                                <Languages className="h-5 w-5 text-dark-text-secondary" aria-hidden="true" />
                              </span>
                            </Listbox.Button>

                            <Transition
                              show={open}
                              as={Fragment}
                              leave="transition ease-in duration-100"
                              leaveFrom="opacity-100"
                              leaveTo="opacity-0"
                            >
                              <Listbox.Options className="absolute bottom-full mb-2 max-h-60 w-full overflow-auto rounded-md bg-dark-primary py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                                {supportedLanguages.map((lang) => (
                                  <Listbox.Option
                                    key={lang.code}
                                    className={({ active }) =>
                                      `relative cursor-default select-none py-2 pl-10 pr-4 ${
                                        active ? 'bg-dark-accent text-white' : 'text-dark-text'
                                      }`
                                    }
                                    value={lang.code}
                                  >
                                    {({ selected, active }) => (
                                      <>
                                        <span
                                          className={`block truncate ${
                                            selected ? 'font-medium' : 'font-normal'
                                          }`}
                                        >
                                          {lang.name}
                                        </span>
                                        {selected ? (
                                          <span
                                            className={`absolute inset-y-0 left-0 flex items-center pl-3 ${
                                              active ? 'text-white' : 'text-dark-accent'
                                            }`}
                                          >
                                            <Check className="h-5 w-5" aria-hidden="true" />
                                          </span>
                                        ) : null}
                                      </>
                                    )}
                                  </Listbox.Option>
                                ))}
                              </Listbox.Options>
                            </Transition>
                          </div>
                        )}
                      </Listbox>
                    </div>
                  </>
                )}
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition>
  );
}