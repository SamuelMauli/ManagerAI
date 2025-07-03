import React, { useState, useEffect, useCallback } from 'react';
import { calendar } from '../services/api';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { format, parseISO } from 'date-fns';
import { ptBR } from 'date-fns/locale';

// Um modal simples para adicionar/editar eventos. Você pode expandir este modal
// para usar componentes de data/hora mais sofisticados (ex: react-datepicker).
const EventModal = ({ isOpen, onClose, onSave, event = null }) => {
    const [summary, setSummary] = useState(event?.summary || '');
    const [description, setDescription] = useState(event?.description || '');
    const [startTime, setStartTime] = useState(event?.start_time ? format(parseISO(event.start_time), "yyyy-MM-dd'T'HH:mm") : '');
    const [endTime, setEndTime] = useState(event?.end_time ? format(parseISO(event.end_time), "yyyy-MM-dd'T'HH:mm") : '');
    const [attendees, setAttendees] = useState(event?.attendees?.map(att => att.email).join(', ') || '');

    useEffect(() => {
        if (event) {
            setSummary(event.summary);
            setDescription(event.description || '');
            setStartTime(event.start_time ? format(parseISO(event.start_time), "yyyy-MM-dd'T'HH:mm") : '');
            setEndTime(event.end_time ? format(parseISO(event.end_time), "yyyy-MM-dd'T'HH:mm") : '');
            setAttendees(event.attendees?.map(att => att.email).join(', ') || '');
        } else {
            // Resetar formulário para novo evento
            setSummary('');
            setDescription('');
            setStartTime('');
            setEndTime('');
            setAttendees('');
        }
    }, [event]);


    if (!isOpen) return null;

    const handleSubmit = (e) => {
        e.preventDefault();
        const eventData = {
            summary,
            description,
            start_time: startTime,
            end_time: endTime,
            attendees: attendees.split(',').map(email => email.trim()).filter(email => email)
        };
        onSave(eventData, event?.id); // Passa o ID se for edição
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <Card className="w-full max-w-md p-6">
                <CardHeader>
                    <CardTitle>{event ? 'Editar Evento' : 'Criar Novo Evento'}</CardTitle>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <Label htmlFor="summary">Título:</Label>
                            <Input id="summary" type="text" value={summary} onChange={(e) => setSummary(e.target.value)} required />
                        </div>
                        <div>
                            <Label htmlFor="description">Descrição:</Label>
                            <Textarea id="description" value={description} onChange={(e) => setDescription(e.target.value)} rows="3" />
                        </div>
                        <div>
                            <Label htmlFor="startTime">Início:</Label>
                            <Input id="startTime" type="datetime-local" value={startTime} onChange={(e) => setStartTime(e.target.value)} required />
                        </div>
                        <div>
                            <Label htmlFor="endTime">Fim:</Label>
                            <Input id="endTime" type="datetime-local" value={endTime} onChange={(e) => setEndTime(e.target.value)} required />
                        </div>
                        <div>
                            <Label htmlFor="attendees">Participantes (e-mails separados por vírgula):</Label>
                            <Input id="attendees" type="text" value={attendees} onChange={(e) => setAttendees(e.target.value)} placeholder="email1@exemplo.com, email2@exemplo.com" />
                        </div>
                        <div className="flex justify-end space-x-2">
                            <Button type="button" variant="outline" onClick={onClose}>Cancelar</Button>
                            <Button type="submit">{event ? 'Salvar Alterações' : 'Criar Evento'}</Button>
                        </div>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
};

const CalendarPage = () => {
    const [todayEvents, setTodayEvents] = useState([]);
    const [allEvents, setAllEvents] = useState([]); // Poderia buscar todos os eventos se necessário
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedEvent, setSelectedEvent] = useState(null); // Para edição

    const fetchTodayEvents = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await calendar.getTodayEvents();
            setTodayEvents(response.data);
        } catch (err) {
            setError('Erro ao carregar eventos de hoje.');
            console.error('Erro ao carregar eventos:', err);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchTodayEvents();
    }, [fetchTodayEvents]);

    const handleCreateNewEvent = () => {
        setSelectedEvent(null); // Garante que é um novo evento
        setIsModalOpen(true);
    };

    const handleEditEvent = (event) => {
        setSelectedEvent(event);
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
        setSelectedEvent(null);
    };

    const handleSaveEvent = async (eventData, eventId = null) => {
        setLoading(true);
        setError(null);
        try {
            if (eventId) {
                await calendar.updateCalendarEvent(eventId, eventData);
                alert('Evento atualizado com sucesso!');
            } else {
                await calendar.createCalendarEvent(eventData);
                alert('Evento criado com sucesso!');
            }
            fetchTodayEvents(); // Recarrega os eventos
            handleCloseModal();
        } catch (err) {
            setError('Erro ao salvar evento. Por favor, tente novamente.');
            console.error('Erro ao salvar evento:', err);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return <div className="text-center py-8">Carregando eventos...</div>;
    }

    if (error) {
        return <div className="text-center py-8 text-red-500">Erro: {error}</div>;
    }

    return (
        <div className="p-6">
            <Card className="mb-6">
                <CardHeader>
                    <CardTitle className="flex justify-between items-center">
                        Eventos do Calendário
                        <Button onClick={handleCreateNewEvent}>Criar Novo Evento</Button>
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <h2 className="text-xl font-bold mb-4">Eventos de Hoje ({format(new Date(), 'dd/MM/yyyy', { locale: ptBR })})</h2>
                    {todayEvents.length > 0 ? (
                        <ul className="space-y-4">
                            {todayEvents.map((event) => (
                                <li key={event.id} className="p-4 border rounded-lg shadow-sm bg-white dark:bg-gray-900">
                                    <div className="flex justify-between items-center">
                                        <h3 className="text-lg font-semibold">{event.summary}</h3>
                                        <Button variant="outline" size="sm" onClick={() => handleEditEvent(event)}>Editar</Button>
                                    </div>
                                    <p className="text-sm text-gray-600 dark:text-gray-300">
                                        Início: {format(parseISO(event.start_time), 'dd/MM/yyyy HH:mm', { locale: ptBR })}
                                    </p>
                                    <p className="text-sm text-gray-600 dark:text-gray-300">
                                        Fim: {format(parseISO(event.end_time), 'dd/MM/yyyy HH:mm', { locale: ptBR })}
                                    </p>
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p className="text-center text-gray-500 dark:text-gray-400">Nenhum evento agendado para hoje.</p>
                    )}
                </CardContent>
            </Card>

            <EventModal
                isOpen={isModalOpen}
                onClose={handleCloseModal}
                onSave={handleSaveEvent}
                event={selectedEvent}
            />
        </div>
    );
};

export default CalendarPage;