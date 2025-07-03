import React, { useEffect, useState } from 'react';
import api from '../api/api';
import toast from 'react-hot-toast';
import { Mail, Calendar, X } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import EmailModal from '../components/dashboard/EmailModal'; // Importe o novo componente

const Dashboard = () => {
  const [userData, setUserData] = useState(null);
  const [unreadEmails, setUnreadEmails] = useState([]);
  const [todayMeetings, setTodayMeetings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isEmailModalOpen, setEmailModalOpen] = useState(false);

  useEffect(() => {
    const fetchAllDashboardData = async () => {
      setLoading(true);
      try {
        const [userRes, emailsRes, calendarRes] = await Promise.all([
          api.get('/dashboard/'),
          api.get('/emails/unread'), 
          api.get('/calendar/today')
        ]);
        setUserData(userRes.data);
        setUnreadEmails(emailsRes.data);
        setTodayMeetings(calendarRes.data);
      } catch (error) {
        if (error.response?.status !== 401) {
          toast.error('Falha ao carregar o dashboard.');
        }
        console.error("Erro no dashboard:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchAllDashboardData();
  }, []);

  const formatTime = (dateTime) => new Date(dateTime).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });

  if (loading && !userData) {
    return <div className="p-8 text-center">Carregando seu dashboard...</div>;
  }

  return (
    <>
      <div className="p-4 md:p-8 space-y-6">
        <h1 className="text-3xl font-bold tracking-tight">
          {userData?.message || 'Bem-vindo(a)!'}
        </h1>

        <div className="grid gap-6 md:grid-cols-2">
          <Card
            onClick={() => unreadEmails.length > 0 && setEmailModalOpen(true)}
            className={unreadEmails.length > 0 ? "cursor-pointer hover:border-primary" : ""}
          >
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-lg font-medium">
                E-mails não Lidos ({unreadEmails.length})
              </CardTitle>
              <Mail className="h-5 w-5 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              {unreadEmails.length > 0 ? (
                <p className="text-sm text-muted-foreground pt-2">
                  Você tem {unreadEmails.length} e-mail{unreadEmails.length > 1 ? 's' : ''} para ler.
                </p>
              ) : (
                <p className="text-sm text-muted-foreground pt-2">Caixa de entrada em dia! 🎉</p>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-lg font-medium">Reuniões de Hoje</CardTitle>
              <Calendar className="h-5 w-5 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              {todayMeetings.length > 0 ? (
                <ul className="space-y-3 pt-2">
                  {todayMeetings.map(meeting => (
                    <li key={meeting.id} className="text-sm border-b pb-2 last:border-b-0">
                      <p className="font-semibold truncate">{meeting.summary}</p>
                      <p className="text-xs text-muted-foreground">
                        {formatTime(meeting.start_time)} - {formatTime(meeting.end_time)}
                      </p>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-muted-foreground pt-2">Nenhuma reunião agendada.</p>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
      
      {isEmailModalOpen && (
        <EmailModal 
          emails={unreadEmails} 
          onClose={() => setEmailModalOpen(false)} 
        />
      )}
    </>
  );
};

export default Dashboard;