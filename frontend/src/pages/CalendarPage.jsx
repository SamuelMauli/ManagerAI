
import React, { useState, useEffect, useMemo } from 'react';
import { Calendar, dateFnsLocalizer } from 'react-big-calendar';
import { format, parse, startOfWeek, getDay } from 'date-fns';
import ptBR from 'date-fns/locale/pt-BR';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import api from '../services/api';
import { useTranslation } from 'react-i18next';

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

  useEffect(() => {
    const fetchAndSetEvents = async () => {
      setLoading(true);
      try {
        // Você precisa criar esta rota no backend que retorna os eventos do DB
        // const response = await api.getCalendarEvents(); 
        // const formattedEvents = response.data.map(event => ({
        //   title: event.summary,
        //   start: new Date(event.start_time),
        //   end: new Date(event.end_time),
        //   allDay: false,
        //   resource: event,
        // }));
        // setEvents(formattedEvents);

        // Placeholder
         setEvents([]);

      } catch (error) {
        console.error("Failed to fetch calendar events:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchAndSetEvents();
  }, []);

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
      <h1 className="text-3xl font-bold mb-6">{t('sidebar.calendar')}</h1>
      <Calendar
        localizer={localizer}
        events={events}
        startAccessor="start"
        endAccessor="end"
        style={{ height: '100%' }}
        messages={messages}
      />
    </div>
  );
};

export default CalendarPage;