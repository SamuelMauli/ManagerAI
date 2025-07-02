import { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { PlusCircle } from 'lucide-react';
import toast from 'react-hot-toast';

// Simula uma chamada de API
const fetchTasksFromApi = async () => {
  // No futuro, isso será uma chamada real: fetch('/api/tasks')
  return [
    { id: 1, title: 'Revisar design do novo App', status: 'Pendente' },
    { id: 2, title: 'Preparar apresentação para a reunião', status: 'Em Progresso' },
    { id: 3, title: 'Corrigir bug no módulo de login', status: 'Concluído' },
  ];
};

const Tasks = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  // Usamos useCallback para evitar que a função seja recriada em cada renderização
  const loadTasks = useCallback(async () => {
    setLoading(true);
    try {
      const data = await fetchTasksFromApi();
      setTasks(data);
    } catch (error) {
      toast.error('Falha ao carregar as tarefas.');
    } finally {
      setLoading(false);
    }
  }, []); // O array vazio significa que a função não tem dependências e não será recriada

  // useEffect para carregar os dados iniciais apenas uma vez
  useEffect(() => {
    loadTasks();
  }, [loadTasks]); // A dependência agora é a função memorizada 'loadTasks'

  if (loading) {
    return <div>Carregando tarefas...</div>;
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>Gerenciador de Tarefas</CardTitle>
        <Button>
          <PlusCircle className="w-4 h-4 mr-2" />
          Nova Tarefa
        </Button>
      </CardHeader>
      <CardContent>
        <ul className="space-y-2">
          {tasks.map((task) => (
            <li key={task.id} className="flex items-center justify-between p-2 rounded-md bg-muted">
              <span>{task.title}</span>
              <span className="px-2 py-1 text-xs text-white bg-primary rounded-full">{task.status}</span>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
};

export default Tasks;