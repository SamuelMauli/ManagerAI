import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import api from '../../services/api';
import { Button } from '@/components/ui/button';
import { Calendar, RefreshCw } from 'lucide-react';
import { format } from 'date-fns';

const CalendarWidget = () => {
    const { t } = useTranslation();
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(false);

    const fetchEvents = async () => {
        setLoading(true);
        try {
            // Primeiro, vamos sincronizar. O ideal é que isso seja um job no backend.
            await api.syncCalendar();
            // Agora, buscamos os eventos. (Você precisa criar esta rota no backend)
            // const response = await api.getCalendarEvents(); 
            // setEvents(response.data);
            
            // Placeholder até a rota existir
            setEvents([]);
            alert("Sincronização do calendário iniciada. A busca de eventos ainda precisa ser implementada no backend (GET /api/v1/calendar/events).");

        } catch (error) {
            console.error("Failed to fetch events", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        // fetchEvents(); // Descomente quando a rota GET existir
    }, []);

    return (
        <div className="space-y-4">
             <Button onClick={fetchEvents} disabled={loading}>
                <RefreshCw className={`mr-2 h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
                {t('dashboard.sync_calendar')}
            </Button>
            {events.length > 0 ? (
                 <ul className="space-y-2">
                    {events.slice(0, 5).map(event => (
                        <li key={event.id} className="flex items-start space-x-3">
                            <Calendar className="h-5 w-5 mt-1 text-primary" />
                            <div>
                                <p className="font-semibold">{event.summary}</p>
                                <p className="text-sm text-muted-foreground">
                                    {format(new Date(event.start_time), 'PPpp')}
                                </p>
                            </div>
                        </li>
                    ))}
                </ul>
            ) : (
                <p className="text-sm text-muted-foreground">{t('dashboard.no_upcoming_events')}</p>
            )}
        </div>
    );
};

export default CalendarWidget;