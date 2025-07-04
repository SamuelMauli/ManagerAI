import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../components/ui/table';
import { Badge } from '../components/ui/badge';
import { Loader2, Inbox, Clock } from 'lucide-react';
import toast from 'react-hot-toast';
import { youtrack } from '../services/api';

// ## COMPONENTE CORRIGIDO ##
// Adicionamos uma verificação de segurança em 'issue.custom_fields'
const BadgeField = ({ issue, fieldName }) => {
    if (!issue?.custom_fields) return <span className="text-slate-500">-</span>; // Guarda de segurança

    const field = issue.custom_fields.find(cf => cf.name === fieldName);
    if (field?.value?.name || field?.value?.login) {
        const valueText = field.value.name || field.value.login;
        const variantMap = {
            "Priority": { "Critical": "destructive", "High": "destructive" },
            "State": { "Fixed": "default", "Done": "default", "In Progress": "secondary" }
        };
        return <Badge variant={variantMap[fieldName]?.[valueText] || "secondary"}>{valueText}</Badge>;
    }
    return <span className="text-slate-500">-</span>;
};

// ## COMPONENTE CORRIGIDO ##
const TimeSpentField = ({ issue }) => {
    if (!issue?.custom_fields) return <span className="text-slate-500">-</span>; // Guarda de segurança

    const field = issue.custom_fields.find(cf => cf.name === 'Spent time' || cf.name === 'Tempo gasto');
    if (field?.value?.minutes) {
        const hours = Math.floor(field.value.minutes / 60);
        const minutes = field.value.minutes % 60;
        return (
            <div className="flex items-center text-sm text-muted-foreground">
                <Clock className="h-4 w-4 mr-1.5" />
                {hours > 0 && `${hours}h `}
                {minutes > 0 && `${minutes}m`}
            </div>
        );
    }
    return <span className="text-slate-500">-</span>;
};


const YoutrackDashboard = () => {
    const [projects, setProjects] = useState([]);
    const [boards, setBoards] = useState([]);
    const [issues, setIssues] = useState([]);
    const [selectedProject, setSelectedProject] = useState(null);
    const [selectedBoard, setSelectedBoard] = useState(null);
    const [loading, setLoading] = useState({ projects: true, boards: false, issues: false });

    // Efeito para carregar projetos
    useEffect(() => {
        setLoading(p => ({ ...p, projects: true }));
        youtrack.getProjects()
            .then(response => setProjects(response.data))
            .catch(() => toast.error('Falha ao carregar projetos.'))
            .finally(() => setLoading(p => ({ ...p, projects: false })));
    }, []);

    // Efeito para carregar boards quando um projeto é selecionado
    useEffect(() => {
        if (!selectedProject?.id) {
            setBoards([]);
            setIssues([]);
            setSelectedBoard(null);
            return;
        }
        setLoading(p => ({ ...p, boards: true }));
        youtrack.getBoards(selectedProject.id)
            .then(response => setBoards(response.data))
            .catch(() => toast.error(`Falha ao carregar boards.`))
            .finally(() => setLoading(p => ({ ...p, boards: false })));
    }, [selectedProject]);

    // Efeito para carregar tarefas com base no projeto e no board selecionado
    useEffect(() => {
        if (!selectedProject?.shortName) {
            setIssues([]); // Limpa os issues se nenhum projeto estiver selecionado
            return;
        }

        const fetchIssues = async () => {
            setLoading(p => ({ ...p, issues: true }));
            const toastId = toast.loading(`Buscando tarefas...`);
            try {
                const response = await youtrack.getIssues(selectedProject.shortName, selectedBoard?.name);
                console.log("Tarefas recebidas da API:", response.data); // Log para depuração
                setIssues(response.data || []); // Garante que 'issues' seja sempre um array
            } catch (error) {
                toast.error(`Falha ao carregar tarefas.`);
                setIssues([]); // Limpa em caso de erro
            } finally {
                toast.dismiss(toastId);
                setLoading(p => ({ ...p, issues: false }));
            }
        };

        fetchIssues();
    }, [selectedProject, selectedBoard]);

    return (
        <div className="container mx-auto p-4 space-y-6">
            <Card>
                <CardHeader>
                    <CardTitle>📊 YouTrack Intelligence Dashboard</CardTitle>
                    <CardDescription>Filtre por projeto e board para analisar seus issues.</CardDescription>
                </CardHeader>
                <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* SELEÇÃO DE PROJETO */}
                    <div className="space-y-2">
                        <label className="text-sm font-medium">Projeto</label>
                        <Select
                            onValueChange={(projectId) => setSelectedProject(projects.find(p => p.id === projectId) || null)}
                            disabled={loading.projects}
                        >
                            <SelectTrigger><SelectValue placeholder={loading.projects ? "Carregando..." : "Selecione um projeto"} /></SelectTrigger>
                            <SelectContent className="max-h-72">
                                {projects.map((p) => <SelectItem key={p.id} value={p.id}>{p.name}</SelectItem>)}
                            </SelectContent>
                        </Select>
                    </div>
                    {/* SELEÇÃO DE BOARD */}
                    <div className="space-y-2">
                        <label className="text-sm font-medium">Board</label>
                        <Select
                            onValueChange={(boardId) => setSelectedBoard(boardId ? boards.find(b => b.id === boardId) : null)}
                            value={selectedBoard?.id || ''}
                            disabled={!selectedProject || loading.boards}
                        >
                            <SelectTrigger>
                                <SelectValue placeholder={loading.boards ? "Carregando..." : "Todos os Issues"} />
                            </SelectTrigger>
                            <SelectContent className="max-h-72">
                                <SelectItem value={null}>Todos os Issues do Projeto</SelectItem>
                                {boards.map((b) => <SelectItem key={b.id} value={b.id}>{b.name}</SelectItem>)}
                            </SelectContent>
                        </Select>
                    </div>
                </CardContent>
            </Card>

            {/* TABELA DE TAREFAS */}
            <Card>
                <CardHeader><CardTitle>{selectedBoard ? `Tarefas do Board: ${selectedBoard.name}` : "Tarefas do Projeto"}</CardTitle></CardHeader>
                <CardContent>
                    {loading.issues ? (
                        <div className="flex justify-center p-10 h-48"><Loader2 className="h-8 w-8 animate-spin" /></div>
                    ) : (
                        <div className="overflow-x-auto">
                            <Table>
                                <TableHeader><TableRow><TableHead>ID</TableHead><TableHead>Resumo</TableHead><TableHead>Status</TableHead><TableHead>Prioridade</TableHead><TableHead>Responsável</TableHead><TableHead>Tempo Gasto</TableHead></TableRow></TableHeader>
                                <TableBody>
                                    {issues.length > 0 ? issues.map(issue => (
                                        <TableRow key={issue.id}>
                                            <TableCell className="font-medium text-muted-foreground">{issue.id_readable}</TableCell>
                                            <TableCell className="font-semibold">{issue.summary}</TableCell>
                                            <TableCell><BadgeField issue={issue} fieldName="State" /></TableCell>
                                            <TableCell><BadgeField issue={issue} fieldName="Priority" /></TableCell>
                                            <TableCell><BadgeField issue={issue} fieldName="Assignee" /></TableCell>
                                            <TableCell><TimeSpentField issue={issue} /></TableCell>
                                        </TableRow>
                                    )) : (
                                        <TableRow><TableCell colSpan={6} className="h-48 text-center text-muted-foreground">
                                            <div className="flex flex-col items-center gap-2">
                                                <Inbox className="h-12 w-12 text-slate-300" />
                                                <span className="font-semibold">Nenhuma tarefa encontrada.</span>
                                                <span>{selectedProject ? "Selecione um board para filtrar ou verifique os issues no YouTrack." : "Selecione um projeto para começar."}</span>
                                            </div>
                                        </TableCell></TableRow>
                                    )}
                                </TableBody>
                            </Table>
                        </div>
                    )}
                </CardContent>
            </Card>
        </div>
    );
};

export default YoutrackDashboard;