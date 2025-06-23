import React from 'react';
import Sidebar from './Sidebar';
import Header from './Header';
import SettingsModal from '../ui/SettingsModal';
import { useUI } from '../../context/UIContext';

// The Layout now accepts a 'children' prop, which will be the
// active page component rendered by the Router.
export default function Layout({ children }) {
  const { isSettingsModalOpen } = useUI();

  return (
    <div className="flex h-screen bg-light-background dark:bg-dark-background">
      <Sidebar />
      <div className="flex flex-1 flex-col overflow-hidden">
        <Header />
        {/* The main content area where pages will be rendered */}
        <main className="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8">
          {children}
        </main>
      </div>
      {isSettingsModalOpen && <SettingsModal />}
    </div>
  );
}