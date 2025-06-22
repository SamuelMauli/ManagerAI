import React, { Suspense } from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';
import './i18n';
import { UIProvider } from './context/UIContext.jsx'; 

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Suspense fallback="Loading...">
      <UIProvider> {/* 2. Envelopar o App */}
        <App />
      </UIProvider>
    </Suspense>
  </React.StrictMode>,
);