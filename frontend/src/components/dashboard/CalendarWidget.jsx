import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { Bell } from 'lucide-react';

export default function ActivityFeed() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Atividade Recente</CardTitle>
        <CardDescription>Você tem 3 tarefas não lidas.</CardDescription>
      </CardHeader>
      <CardContent className="grid gap-4">
        <div className="flex items-center gap-4 p-2 -mx-2 rounded-lg hover:bg-muted">
          <Bell className="w-5 h-5" />
          <div className="grid gap-1">
            <p className="text-sm font-medium">Nova tarefa atribuída</p>
            <p className="text-sm text-muted-foreground">Revisar o design do novo app.</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}