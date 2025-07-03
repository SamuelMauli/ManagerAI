import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { Calendar, dateFnsLocalizer } from 'react-big-calendar';
import { format, parse, startOfWeek, getDay } from 'date-fns';
import ptBR from 'date-fns/locale/pt-BR';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import api from '../services/api'; 
import { useTranslation } from 'react-i18next';
import { PlusCircle, RefreshCw } from 'lucide-react'; // Adicionado RefreshCw para loading

const locales = {
  'pt-BR': ptBR,
};

const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek: (date) => startOfWeek(date, { locale: ptBR }),
  getDay,
  locales,
});

const CalendarPage = () => {
  const { t } = useTranslation();
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showEventModal, setShowEventModal] = useState(false); // Estado para controlar a visibilidade do modal de evento

  // Função para buscar eventos do Google Calendar
  const fetchCalendarEvents = useCallback(async () => {
    setLoading(true);
    try {
      // Chama o endpoint do backend que busca eventos do Google Calendar para hoje
      const response = await api.get('/calendar/today'); 
      
      // Mapeia os eventos do backend para o formato do react-big-calendar
      // O backend já retorna 'start_time' e 'end_time' em formato ISO,
      // então basta converter para objetos Date.
      const formattedEvents = response.data.map(event => ({
        id: event.id,
        title: event.summary, // O campo 'summary' do Google Calendar é o título
        start: new Date(event.start_time),
        end: new Date(event.end_time),
        allDay: false, // Assumimos que eventos do Google Calendar têm horários específicos
        resource: event, // Armazena o objeto do evento completo, se precisar
      }));
      setEvents(formattedEvents);
    } catch (error) {
      console.error("Failed to fetch Google Calendar events:", error);
      toast.error(t('calendar.errors.fetchEvents')); // Adicionar esta chave de tradução
    } finally {
      setLoading(false);
    }
  }, [t]);

  useEffect(() => {
    fetchCalendarEvents();
  }, [fetchCalendarEvents]);

  // Função para lidar com a criação de um novo evento (placeholder)
  const handleNewEvent = async (newEventData) => {
    // Aqui você integraria a API do Google Calendar para criar um evento.
    // Por enquanto, é um placeholder.
    console.log("Tentativa de criar novo evento:", newEventData);
    toast.info(t('common.featureComingSoon')); // Usar tradução existente
    setShowEventModal(false);
    // Após a criação (ou simulação), recarregar os eventos
    fetchCalendarEvents();
  };

  // Personaliza o estilo dos eventos no calendário (opcional)
  const eventPropGetter = (event, start, end, isSelected) => {
    let newStyle = {
      // Exemplo: Cores diferentes baseadas em alguma propriedade do evento
      backgroundColor: '#3B82F6', // Azul padrão
      color: 'white',
      borderRadius: '4px',
      border: 'none',
      // Você pode adicionar mais lógica de estilo aqui, se desejar,
      // baseada em event.resource (o objeto original do evento Google)
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
    return (
        <div className="flex justify-center items-center h-full">
            <RefreshCw size={32} className="animate-spin text-dark-accent" />
            <p className="ml-2 text-dark-text">{t('loading')}...</p>
        </div>
    );
  }

  return (
    <div className="p-6 h-[calc(100vh-80px)]">
      <div className="flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold">{t('sidebar.calendar')}</h1>
          <p className="mt-2 text-lg text-muted-foreground">
            {t('calendar.subtitle')}
          </p>
        </div>
        <button
          onClick={() => setShowEventModal(true)}
          className="inline-flex items-center gap-2 rounded-lg bg-dark-accent px-4 py-2 font-semibold text-white transition-colors hover:bg-dark-accent/80"
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

      {/* Placeholder para o modal de criação de evento */}
      {showEventModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-card p-8 rounded-lg shadow-xl w-full max-w-md text-card-foreground">
            <h2 className="text-2xl font-bold mb-4">{t('calendar.createEventTitle')}</h2>
            <p className="text-muted-foreground mb-4">
              {t('common.contentPlaceholder')} Implementar formulário de evento aqui.
            </p>
            <div className="flex justify-end gap-2">
              <Button
                onClick={() => setShowEventModal(false)}
                variant="outline"
              >
                {t('common.cancel')}
              </Button>
              <Button
                onClick={() => handleNewEvent({ title: 'Novo Evento', description: 'Descrição do evento', start_time: new Date().toISOString(), end_time: new Date().toISOString() })}
                disabled // Desabilitado até que a funcionalidade real seja implementada
              >
                {t('common.save')}
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CalendarPage;