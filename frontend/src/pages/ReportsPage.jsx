import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import api from '../services/api';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { FileText, Send } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

const ReportsPage = () => {
  const { t } = useTranslation();
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState('');
  const [prompt, setPrompt] = useState('Gere um relatório executivo sobre o status deste projeto, destacando pontos de bloqueio, tarefas críticas e o progresso geral.');
  const [report, setReport] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await api.getYoutrackProjects();
        setProjects(response.data);
      } catch (error) {
        console.error("Failed to fetch projects", error);
      }
    };
    fetchProjects();
  }, []);

  const handleGenerateReport = async () => {
    if (!selectedProject) {
      alert(t('reports.select_project_alert'));
      return;
    }
    setLoading(true);
    setReport('');
    try {
      const response = await api.generateTasksByProjectReport({
        project_id: selectedProject,
        user_prompt: prompt,
      });
      setReport(response.data.content);
    } catch (error) {
      console.error("Failed to generate report", error);
      setReport(t('reports.generation_error'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">{t('sidebar.reports')}</h1>
      
      <Card>
        <CardHeader>
          <CardTitle>{t('reports.configure_report')}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="project-select" className="block text-sm font-medium mb-1">{t('reports.select_project')}</label>
              <Select onValueChange={setSelectedProject} value={selectedProject}>
                <SelectTrigger id="project-select">
                  <SelectValue placeholder={t('reports.select_project_placeholder')} />
                </SelectTrigger>
                <SelectContent>
                  {projects.map((p) => (
                    <SelectItem key={p.id} value={p.id}>{p.name}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
          <div>
            <label htmlFor="prompt-textarea" className="block text-sm font-medium mb-1">{t('reports.report_objective')}</label>
            <Textarea
              id="prompt-textarea"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder={t('reports.prompt_placeholder')}
              rows={4}
            />
          </div>
          <Button onClick={handleGenerateReport} disabled={loading || !selectedProject}>
            <Send className={`mr-2 h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
            {loading ? t('reports.generating') : t('reports.generate_report')}
          </Button>
        </CardContent>
      </Card>

      {report && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <FileText className="mr-2 h-5 w-5" />
              {t('reports.generated_report')}
            </CardTitle>
          </CardHeader>
          <CardContent className="prose dark:prose-invert max-w-none">
            <ReactMarkdown>{report}</ReactMarkdown>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default ReportsPage;