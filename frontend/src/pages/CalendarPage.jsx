import React, { useState, useEffect, useMemo } from 'react';
import { Calendar, dateFnsLocalizer } from 'react-big-calendar';
import { format, parse, startOfWeek, getDay } from 'date-fns';
import ptBR from 'date-fns/locale/pt-BR';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import api from '../services/api'; // Importe o serviço de API
import { useTranslation } from 'react-i18next';
import { PlusCircle } from 'lucide-react'; // Ícone para o botão "Nova Tarefa"

const locales = {
  'pt-BR': ptBR,
};

const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek: () => startOfWeek(new Date(), { locale: ptBR }),
  getDay,
  locales,
});

const CalendarPage = () => {
  const { t } = useTranslation();
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showTaskModal, setShowTaskModal] = useState(false); // Estado para controlar a visibilidade do modal

  const fetchTasks = async () => {
    setLoading(true);
    try {
      const response = await api.getTasks(); // Chama o endpoint de tarefas
      // Mapeia as tarefas do backend para o formato do react-big-calendar
      const formattedTasks = response.data.map(task => ({
        id: task.id,
        title: task.title,
        start: new Date(task.due_date || task.created_at), // Usa due_date se existir, senão created_at
        end: task.due_date ? new Date(task.due_date) : new Date(task.created_at), // Para eventos de um dia, start e end são os mesmos
        allDay: true, // Ou false, dependendo se sua tarefa tem horário específico
        resource: task, // Armazena o objeto da tarefa completa, se precisar
        isCompleted: task.completed, // Adiciona propriedade para styling
      }));
      setEvents(formattedTasks);
    } catch (error) {
      console.error("Failed to fetch tasks for calendar:", error);
      // Você pode adicionar um tratamento de erro mais amigável aqui, como uma notificação
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []); // Executa apenas na montagem do componente

  // Função para lidar com a criação de uma nova tarefa (chamada pelo modal)
  const handleNewTask = async (newTaskData) => {
    try {
      await api.createTask(newTaskData); // Chama o endpoint para criar tarefa
      setShowTaskModal(false); // Fecha o modal
      fetchTasks(); // Recarrega as tarefas para atualizar o calendário
    } catch (error) {
      console.error("Failed to create task:", error);
      // Tratar erro na criação da tarefa
    }
  };

  // Personaliza o estilo dos eventos no calendário (opcional)
  const eventPropGetter = (event, start, end, isSelected) => {
    let newStyle = {
      backgroundColor: event.isCompleted ? '#6b7280' : '#3B82F6', // Cinza para completo, Azul para não completo
      color: 'white',
      borderRadius: '0px',
      border: 'none',
    };
    return {
      className: '',
      style: newStyle
    };
  };

  const { messages } = useMemo(() => ({
    messages: {
      allDay: t('calendar.allDay'),
      previous: t('calendar.previous'),
      next: t('calendar.next'),
      today: t('calendar.today'),
      month: t('calendar.month'),
      week: t('calendar.week'),
      day: t('calendar.day'),
      agenda: t('calendar.agenda'),
      date: t('calendar.date'),
      time: t('calendar.time'),
      event: t('calendar.event'),
    }
  }), [t]);

  if (loading) {
    return <div className="p-6">{t('loading')}...</div>;
  }

  return (
    <div className="p-6 h-[calc(100vh-80px)]">
      <div className="flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold">{t('sidebar.calendar')}</h1>
          <p className="mt-2 text-lg text-dark-text-secondary">
            {t('calendar.subtitle')}
          </p>
        </div>
        <button
          onClick={() => setShowTaskModal(true)}
          className="inline-flex items-center gap-2 rounded-lg bg-dark-accent px-4 py-2 font-semibold text-white transition-colors hover:bg-dark-accent-hover"
        >
          <PlusCircle size={20} />
          {t('calendar.newButton')}
        </button>
      </div>

      <Calendar
        localizer={localizer}
        events={events}
        startAccessor="start"
        endAccessor="end"
        style={{ height: 'calc(100% - 60px)' }}
        messages={messages}
        eventPropGetter={eventPropGetter} // Aplica estilos personalizados
      />

      {/* Placeholder para o modal de criação de tarefa */}
      {showTaskModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-dark-card p-8 rounded-lg shadow-xl w-full max-w-md">
            <h2 className="text-2xl font-bold mb-4 text-dark-text">{t('calendar.createTaskTitle')}</h2>
            {/* Aqui você adicionará o formulário para criar a tarefa */}
            <p className="text-dark-text-secondary mb-4">
              {t('common.contentPlaceholder')} Implementar formulário de tarefa aqui.
            </p>
            <div className="flex justify-end gap-2">
              <button
                onClick={() => setShowTaskModal(false)}
                className="px-4 py-2 rounded-lg bg-gray-600 text-white hover:bg-gray-700"
              >
                {t('common.cancel')}
              </button>
              {/* Botão de salvar (desabilitado por enquanto) */}
              <button
                // onClick={() => handleNewTask({ title: 'Nova Tarefa', description: 'Descrição da tarefa', due_date: new Date().toISOString() })}
                className="px-4 py-2 rounded-lg bg-dark-accent text-white opacity-50 cursor-not-allowed"
                disabled
              >
                {t('common.save')}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CalendarPage;