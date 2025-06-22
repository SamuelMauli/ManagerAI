import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import HttpApi from 'i18next-http-backend';

i18n
  .use(HttpApi) // Carrega traduções de um backend (ex: /locales/en/translation.json)
  .use(LanguageDetector) // Detecta o idioma do usuário
  .use(initReactI18next) // Passa a instância do i18n para o react-i18next
  .init({
    supportedLngs: ['en', 'pt', 'es', 'de'],
    fallbackLng: 'en',
    detection: {
      order: ['querystring', 'cookie', 'localStorage', 'navigator', 'htmlTag'],
      caches: ['cookie'],
    },
    backend: {
      loadPath: '/locales/{{lng}}/translation.json',
    },
    react: {
      useSuspense: true, // Recomendado para carregar os arquivos de tradução
    },
  });

export default i18n;
