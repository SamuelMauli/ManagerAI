import { Dialog, Transition, Menu } from '@headlessui/react';
import { Fragment, useState, useEffect } from 'react';
import { useUI } from '../../context/UIContext';
import { useTranslation } from 'react-i18next';
import toast from 'react-hot-toast';
import api from '../../services/api';
import { X, Languages, Check, RefreshCw, Save, LoaderCircle } from 'lucide-react';

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

  const currentLanguage = supportedLanguages.find(lang => lang.code === i18n.language);

  useEffect(() => {
    if (isSettingsModalOpen) {
      const loadAllSettings = async () => {
        setIsLoading(true);
        try {
          const [youtrackRes, emailRes] = await Promise.all([
            getYouTrackSettings(),
            getEmailSettings(),
          ]);

          if (youtrackRes.data) {
            setYouTrackUrl(youtrackRes.data.url || '');
            setYouTrackToken(youtrackRes.data.token || '');
          }

          if (emailRes.data) {
            setEmailAddress(emailRes.data.email || '');
          }
        } catch (error) {
          console.error('Could not load settings.', error);
          toast.error(t('settings.errors.load'));
        } finally {
          setIsLoading(false);
        }
      };
      loadAllSettings();
    }
  }, [isSettingsModalOpen, t]);

  const handleSaveYouTrack = async () => {
    setIsSavingYouTrack(true);
    const promise = saveYouTrackSettings({ url: youTrackUrl, token: youTrackToken });
    
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
      success: t('jobs.successYouTrack'),
      error: t('jobs.errors.syncYouTrack'),
    }).finally(() => setIsSyncingYouTrack(false));
  };

  const handleSaveEmail = async () => {
    setIsSavingEmail(true);
    const promise = saveEmailSettings({ email: emailAddress, password: emailPassword });
    
    toast.promise(promise, {
      loading: t('settings.savingEmail'),
      success: t('settings.successEmail'),
      error: t('settings.errors.saveEmail'),
    }).finally(() => {
      setEmailPassword('');
      setIsSavingEmail(false);
    });
  };

  const handleRunEmailJob = async () => {
    setIsSyncingEmail(true);
    const promise = runEmailJob();

    toast.promise(promise, {
      loading: t('jobs.syncing'),
      success: t('jobs.successEmail'),
      error: t('jobs.errors.syncEmail'),
    }).finally(() => setIsSyncingEmail(false));
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
                      <Menu as="div" className="relative inline-block w-full text-left">
                        <div>
                          <Menu.Button className="inline-flex w-full justify-between rounded-md border border-white/20 bg-dark-background px-4 py-2 text-sm font-medium text-dark-text hover:bg-dark-primary focus:outline-none focus-visible:ring-2 focus-visible:ring-dark-accent">
                            {currentLanguage?.name || t('settings.languagePlaceholder')}
                            <Languages className="ml-2 -mr-1 h-5 w-5 text-dark-text-secondary" aria-hidden="true"/>
                          </Menu.Button>
                        </div>
                        <Transition as={Fragment} enter="transition ease-out duration-100" enterFrom="transform opacity-0 scale-95" enterTo="transform opacity-100 scale-100" leave="transition ease-in duration-75" leaveFrom="transform opacity-100 scale-100" leaveTo="transform opacity-0 scale-95">
                          <Menu.Items className="absolute bottom-full mb-2 w-full origin-bottom-right divide-y divide-gray-100/10 rounded-md bg-dark-primary shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                            <div className="px-1 py-1 ">
                              {supportedLanguages.map((lang) => (
                                <Menu.Item key={lang.code}>
                                  {({ active }) => (
                                    <button onClick={() => i18n.changeLanguage(lang.code)} className={`${active ? 'bg-dark-accent text-white' : 'text-dark-text'} group flex w-full items-center rounded-md px-2 py-2 text-sm`}>
                                      {i18n.language === lang.code ? <Check className="mr-2 h-5 w-5" /> : <span className="mr-2 h-5 w-5" />}
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