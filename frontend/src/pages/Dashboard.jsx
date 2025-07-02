import { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Mail, Loader2 } from 'lucide-react';
import toast from 'react-hot-toast';

const fetchUnreadEmails = async (token) => {
  const response = await fetch(`http://localhost:8000/emails/unread`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Falha ao buscar e-mails.');
  }
  return response.json();
};

const Dashboard = () => {
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadEmails = useCallback(async () => {
    setLoading(true);
    const token = localStorage.getItem('google_access_token');
    
    if (!token) {
        toast.error("Sessão não encontrada. Faça login novamente.");
        setLoading(false);
        return;
    }

    try {
      const data = await fetchUnreadEmails(token);
      setEmails(data.emails);
    } catch (error) {
      toast.error(error.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadEmails();
  }, [loadEmails]);

  return (
    <Card className="col-span-1 lg:col-span-4">
      <CardHeader className="flex flex-row items-center gap-2">
        <Mail className="w-5 h-5 text-muted-foreground" />
        <CardTitle>Caixa de Entrada - Não Lidos</CardTitle>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="flex items-center justify-center p-8">
            <Loader2 className="w-8 h-8 animate-spin text-muted-foreground" />
          </div>
        ) : emails.length > 0 ? (
          <ul className="space-y-4">
            {emails.map((email) => (
              <li key={email.id} className="p-3 transition-colors rounded-lg hover:bg-muted">
                <p className="font-semibold text-sm truncate">{email.from}</p>
                <p className="font-medium">{email.subject}</p>
                <p className="text-xs text-muted-foreground truncate">{email.snippet}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p className="py-8 text-center text-muted-foreground">Nenhum e-mail não lido. Caixa de entrada limpa!</p>
        )}
      </CardContent>
    </Card>
  );
};

export default Dashboard;