import React, { useState, useEffect, useCallback } from 'react';
import { emails } from '../services/api';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Textarea } from '../components/ui/textarea';
import { Label } from '../components/ui/label';
import { format, parseISO } from 'date-fns';
import { ptBR } from 'date-fns/locale';

const EmailsPage = () => {
    const [emailList, setEmailList] = useState([]);
    const [unreadEmails, setUnreadEmails] = useState([]);
    const [selectedEmail, setSelectedEmail] = useState(null);
    const [showSendEmailForm, setShowSendEmailForm] = useState(false);
    const [sendEmailData, setSendEmailData] = useState({ to: '', subject: '', body: '', is_html: false, in_reply_to_id: null, thread_id: null });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [currentView, setCurrentView] = useState('all'); // 'all' ou 'unread'

    const fetchEmails = useCallback(async (view) => {
        setLoading(true);
        setError(null);
        try {
            let response;
            if (view === 'unread') {
                response = await emails.getUnreadEmails();
                setUnreadEmails(response.data);
                setEmailList([]); // Limpa a lista de todos os e-mails
            } else {
                response = await emails.getPaginatedEmails();
                setEmailList(response.data);
                setUnreadEmails([]); // Limpa a lista de não lidos
            }
            setSelectedEmail(null); // Reseta a seleção ao trocar de view ou recarregar
        } catch (err) {
            setError('Erro ao carregar e-mails. Por favor, tente novamente.');
            console.error('Erro ao carregar e-mails:', err);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchEmails(currentView);
    }, [fetchEmails, currentView]);

    const handleSyncEmails = async () => {
        setLoading(true);
        setError(null);
        try {
            await emails.syncEmails();
            alert('Sincronização de e-mails iniciada em segundo plano.');
            // Após a sincronização, recarregue os e-mails após um pequeno atraso
            setTimeout(() => fetchEmails(currentView), 3000); 
        } catch (err) {
            setError('Erro ao iniciar sincronização.');
            console.error('Erro ao sincronizar e-mails:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleEmailClick = async (emailId, threadId) => {
        setLoading(true);
        setError(null);
        try {
            // Se já for uma thread, buscamos a thread completa
            const emailThreadResponse = await emails.getEmailThread(threadId);
            const threadEmails = emailThreadResponse.data.sort((a, b) => new Date(a.received_at) - new Date(b.received_at));
            setSelectedEmail({ id: emailId, thread: threadEmails });

            // Marcar o e-mail clicado como lido
            if (threadEmails.find(e => e.id === emailId)?.is_read === false) {
                await emails.markEmailAsRead(emailId);
                fetchEmails(currentView); // Recarrega para atualizar o status
            }
        } catch (err) {
            setError('Erro ao carregar detalhes do e-mail/thread.');
            console.error('Erro ao carregar detalhes do e-mail:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleBackToList = () => {
        setSelectedEmail(null);
    };

    const handleSendEmailChange = (e) => {
        const { name, value, type, checked } = e.target;
        setSendEmailData(prevState => ({
            ...prevState,
            [name]: type === 'checkbox' ? checked : value
        }));
    };

    const handleSendEmailSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            await emails.sendEmail(sendEmailData);
            alert('E-mail enviado com sucesso!');
            setShowSendEmailForm(false);
            setSendEmailData({ to: '', subject: '', body: '', is_html: false, in_reply_to_id: null, thread_id: null });
        } catch (err) {
            setError('Erro ao enviar e-mail. Por favor, verifique os dados.');
            console.error('Erro ao enviar e-mail:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleReply = () => {
        if (selectedEmail && selectedEmail.thread && selectedEmail.thread.length > 0) {
            const originalEmail = selectedEmail.thread[selectedEmail.thread.length - 1]; // Último e-mail na thread
            setSendEmailData({
                to: originalEmail.sender.match(/<(.*?)>/)?.[1] || originalEmail.sender, // Extrai o email se estiver em formato "Nome <email>"
                subject: `Re: ${originalEmail.subject}`,
                body: `\n\n--- Original Message ---\nFrom: ${originalEmail.sender}\nTo: ${originalEmail.to}\nSubject: ${originalEmail.subject}\nDate: ${format(parseISO(originalEmail.received_at), 'dd/MM/yyyy HH:mm', { locale: ptBR })}\n\n${originalEmail.body}`,
                is_html: false, // Pode ser ajustado se o corpo original for HTML
                in_reply_to_id: originalEmail.google_email_id,
                thread_id: originalEmail.thread_id
            });
            setShowSendEmailForm(true);
        }
    };

    if (loading) {
        return <div className="text-center py-8">Carregando e-mails...</div>;
    }

    if (error) {
        return <div className="text-center py-8 text-red-500">Erro: {error}</div>;
    }

    return (
        <div className="p-6">
            <Card className="mb-6">
                <CardHeader>
                    <CardTitle className="flex justify-between items-center">
                        E-mails
                        <div className="space-x-2">
                            <Button onClick={() => setCurrentView('all')} variant={currentView === 'all' ? 'default' : 'outline'}>Todos</Button>
                            <Button onClick={() => setCurrentView('unread')} variant={currentView === 'unread' ? 'default' : 'outline'}>Não Lidos ({unreadEmails.length})</Button>
                            <Button onClick={handleSyncEmails}>Sincronizar E-mails</Button>
                            <Button onClick={() => setShowSendEmailForm(true)}>Enviar Novo E-mail</Button>
                        </div>
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    {showSendEmailForm && (
                        <div className="mb-6 p-4 border rounded-lg bg-gray-50 dark:bg-gray-800">
                            <h3 className="text-lg font-semibold mb-4">Enviar E-mail</h3>
                            <form onSubmit={handleSendEmailSubmit} className="space-y-4">
                                <div>
                                    <Label htmlFor="to">Para:</Label>
                                    <Input id="to" name="to" type="email" value={sendEmailData.to} onChange={handleSendEmailChange} required />
                                </div>
                                <div>
                                    <Label htmlFor="subject">Assunto:</Label>
                                    <Input id="subject" name="subject" type="text" value={sendEmailData.subject} onChange={handleSendEmailChange} required />
                                </div>
                                <div>
                                    <Label htmlFor="body">Corpo:</Label>
                                    <Textarea id="body" name="body" value={sendEmailData.body} onChange={handleSendEmailChange} rows="6" required />
                                </div>
                                <div className="flex items-center space-x-2">
                                    <input type="checkbox" id="is_html" name="is_html" checked={sendEmailData.is_html} onChange={handleSendEmailChange} />
                                    <Label htmlFor="is_html">Conteúdo HTML?</Label>
                                </div>
                                <div className="flex justify-end space-x-2">
                                    <Button type="button" variant="outline" onClick={() => setShowSendEmailForm(false)}>Cancelar</Button>
                                    <Button type="submit">Enviar</Button>
                                </div>
                            </form>
                        </div>
                    )}

                    {selectedEmail ? (
                        <div>
                            <Button onClick={handleBackToList} className="mb-4">Voltar para a lista</Button>
                            <Button onClick={handleReply} className="mb-4 ml-2">Responder</Button>
                            <h2 className="text-xl font-bold mb-4">Conversa de E-mail</h2>
                            {selectedEmail.thread.map((email, index) => (
                                <Card key={email.id} className="mb-4">
                                    <CardHeader className="bg-gray-100 dark:bg-gray-700 rounded-t-lg">
                                        <CardTitle className="text-lg">Assunto: {email.subject}</CardTitle>
                                        <p className="text-sm text-gray-600 dark:text-gray-300">De: {email.sender}</p>
                                        <p className="text-sm text-gray-600 dark:text-gray-300">Recebido em: {format(parseISO(email.received_at), 'dd/MM/yyyy HH:mm', { locale: ptBR })}</p>
                                    </CardHeader>
                                    <CardContent className="pt-4">
                                        <p className="whitespace-pre-wrap">{email.body || email.snippet}</p>
                                    </CardContent>
                                </Card>
                            ))}
                        </div>
                    ) : (
                        <ul className="space-y-4">
                            {(currentView === 'all' ? emailList : unreadEmails).map((email) => (
                                <li 
                                    key={email.id} 
                                    className={`p-4 border rounded-lg shadow-sm cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 ${email.is_read ? 'bg-white dark:bg-gray-900' : 'bg-blue-50 dark:bg-blue-950 font-semibold'}`}
                                    onClick={() => handleEmailClick(email.id, email.thread_id)}
                                >
                                    <div className="flex justify-between items-center">
                                        <h3 className="text-lg font-semibold">{email.subject || 'Sem Assunto'}</h3>
                                        <span className="text-sm text-gray-500 dark:text-gray-400">
                                            {format(parseISO(email.received_at), 'dd/MM/yyyy HH:mm', { locale: ptBR })}
                                        </span>
                                    </div>
                                    <p className="text-gray-600 dark:text-gray-300">De: {email.sender}</p>
                                    <p className="text-gray-500 dark:text-gray-400 text-sm mt-1">{email.snippet}</p>
                                </li>
                            ))}
                            {emailList.length === 0 && unreadEmails.length === 0 && (
                                <p className="text-center text-gray-500 dark:text-gray-400">Nenhum e-mail encontrado.</p>
                            )}
                        </ul>
                    )}
                </CardContent>
            </Card>
        </div>
    );
};

export default EmailsPage;