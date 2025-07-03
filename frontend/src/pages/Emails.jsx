import React, { useState, useEffect, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { PlusCircle, Mail, RefreshCw, CheckCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Button } from '../components/ui/button';
import api from '../services/api';
import toast from 'react-hot-toast';

const Emails = () => {
  const { t } = useTranslation();
  const [unreadEmails, setUnreadEmails] = useState([]);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);

  // Função para carregar e-mails não lidos
  const fetchUnreadEmails = useCallback(async () => {
    setLoading(true);
    try {
      const response = await api.getUnreadEmails();
      setUnreadEmails(response.data);
    } catch (error) {
      console.error("Failed to fetch unread emails:", error);
      toast.error(t('emails.errors.fetch'));
    } finally {
      setLoading(false);
    }
  }, [t]);

  // Função para sincronizar e-mails
  const handleSyncEmails = async () => {
    setSyncing(true);
    const promise = api.syncEmails();
    toast.promise(promise, {
      loading: t('jobs.syncing'),
      success: t('jobs.emailJobSuccess'),
      error: t('jobs.emailJobError'),
    }).finally(() => {
      setSyncing(false);
      // Após a sincronização, recarregue os e-mails para ver os novos
      fetchUnreadEmails();
    });
  };

  // Função para marcar um e-mail como lido
  const handleMarkAsRead = async (emailId) => {
    try {
      await api.markEmailAsRead(emailId);
      toast.success(t('emails.markAsReadSuccess'));
      fetchUnreadEmails(); // Recarrega a lista para remover o e-mail lido
    } catch (error) {
      console.error("Failed to mark email as read:", error);
      toast.error(t('emails.errors.markAsRead'));
    }
  };

  useEffect(() => {
    fetchUnreadEmails();
  }, [fetchUnreadEmails]);

  const formatDateTime = (dateTime) => {
    if (!dateTime) return '';
    // Certifica-se de que é um objeto Date para formatar
    const date = new Date(dateTime); 
    // Opções de formatação para exibir de forma amigável
    return date.toLocaleString('pt-BR', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold">{t('sidebar.emails')}</h1>
          <p className="mt-2 text-lg text-muted-foreground">
            {t('emails.subtitle')}
          </p>
        </div>
        <div className="flex gap-2">
            <Button 
                onClick={handleSyncEmails} 
                disabled={syncing}
                className="inline-flex items-center gap-2"
            >
                {syncing ? <RefreshCw size={20} className="animate-spin" /> : <RefreshCw size={20} />}
                {syncing ? t('jobs.syncing') : t('jobs.emailUpdateButton')}
            </Button>
            {/* Você pode adicionar um botão para "Novo E-mail" aqui se houver uma funcionalidade de envio */}
            <Button className="inline-flex items-center gap-2">
                <PlusCircle size={20} />
                {t('emails.newButton')}
            </Button>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Mail className="mr-2 h-5 w-5" />
            {t('dashboard.unreadEmails')} ({unreadEmails.length})
          </CardTitle>
          <CardDescription>
            {t('emails.listDescription')}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="flex justify-center items-center h-48">
              <RefreshCw size={32} className="animate-spin text-muted-foreground" />
            </div>
          ) : unreadEmails.length === 0 ? (
            <p className="text-center text-muted-foreground py-8">{t('emails.noUnreadEmails')}</p>
          ) : (
            <ul className="divide-y divide-border">
              {unreadEmails.map((email) => (
                <li key={email.id} className="py-4 flex items-center justify-between">
                  <div className="flex-1 min-w-0 pr-4">
                    <p className="font-semibold text-lg truncate">{email.subject || t('emails.noSubject')}</p>
                    <p className="text-sm text-muted-foreground truncate">De: {email.sender}</p>
                    <p className="text-xs text-muted-foreground mt-1">{formatDateTime(email.received_at)}</p>
                    <p className="text-sm mt-2 text-foreground line-clamp-2">{email.snippet}</p>
                  </div>
                  <Button 
                    variant="outline" 
                    size="icon" 
                    onClick={() => handleMarkAsRead(email.id)}
                    title={t('emails.markAsRead')}
                  >
                    <CheckCircle className="h-5 w-5 text-green-500" />
                  </Button>
                </li>
              ))}
            </ul>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Emails;