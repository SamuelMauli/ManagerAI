import React, { useEffect, useState } from 'react';
import api from '../api/api'; // Verifique se este caminho está correto
import toast from 'react-hot-toast';
import { Mail, Calendar } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';

const Dashboard = () => {
  const [userData, setUserData] = useState(null);
  const [unreadEmails, setUnreadEmails] = useState([]);
  const [todayMeetings, setTodayMeetings] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAllDashboardData = async () => {
      setLoading(true);

      try {
        // As chamadas permanecem as mesmas. O interceptor fará o trabalho.
        const [userRes, emailsRes, calendarRes] = await Promise.all([
          api.get('/dashboard/'),
          api.get('/emails/unread'),
          api.get('/calendar/today')
        ]);

        setUserData(userRes.data);
        setUnreadEmails(emailsRes.data);
        setTodayMeetings(calendarRes.data);

      } catch (error) {
        // O interceptor de erro já vai redirecionar em caso de 401.
        // Este toast pode nem ser exibido, mas é bom mantê-lo para outros erros.
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

  // O resto do seu componente de renderização permanece o mesmo...
  
  const formatTime = (dateTime) => new Date(dateTime).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });

  if (loading && !userData) { // Mostra o carregamento apenas na primeira vez
    return <div className="p-8 text-center">Carregando seu dashboard...</div>;
  }

  return (
    <div className="p-4 md:p-8 space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">
        {userData?.message || 'Bem-vindo(a)!'}
      </h1>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-lg font-medium">E-mails não Lidos</CardTitle>
            <Mail className="h-5 w-5 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            {unreadEmails.length > 0 ? (
              <ul className="space-y-3 pt-2">
                {unreadEmails.map(email => (
                  <li key={email.google_email_id} className="text-sm border-b pb-2 last:border-b-0">
                    <p className="font-semibold truncate">{email.subject}</p>
                    <p className="text-xs text-muted-foreground">De: {email.sender}</p>
                  </li>
                ))}
              </ul>
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
  );
};

export default Dashboard;