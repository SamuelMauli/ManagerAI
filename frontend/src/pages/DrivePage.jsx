// frontend/src/pages/DrivePage.jsx (Exemplo - você precisará implementar a UI)
import React, { useState } from 'react';
import { drive } from '../services/api';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Button } from '../components/ui/button';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';

const DrivePage = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState([]);
    const [fileContent, setFileContent] = useState(null);
    const [createFileData, setCreateFileData] = useState({ name: '', mimeType: '', content: '' });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSearch = async () => {
        setLoading(true);
        setError(null);
        setSearchResults([]);
        setFileContent(null);
        try {
            const response = await drive.searchFiles(searchQuery);
            setSearchResults(response.data);
        } catch (err) {
            setError('Erro ao buscar arquivos no Drive.');
            console.error('Erro ao buscar arquivos:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleGetFileContent = async (fileId) => {
        setLoading(true);
        setError(null);
        setFileContent(null);
        try {
            const response = await drive.getFileContent(fileId);
            setFileContent(response.data);
        } catch (err) {
            setError('Erro ao obter o conteúdo do arquivo.');
            console.error('Erro ao obter conteúdo:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleCreateFileChange = (e) => {
        const { name, value } = e.target;
        setCreateFileData(prevState => ({ ...prevState, [name]: value }));
    };

    const handleCreateFile = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            const response = await drive.createFile(createFileData.name, createFileData.mimeType, createFileData.content);
            alert(`Arquivo "${response.data.name}" criado com sucesso! Link: ${response.data.web_view_link}`);
            setCreateFileData({ name: '', mimeType: '', content: '' });
        } catch (err) {
            setError('Erro ao criar arquivo no Drive.');
            console.error('Erro ao criar arquivo:', err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-6">
            <Card className="mb-6">
                <CardHeader><CardTitle>Google Drive - Buscar Arquivos</CardTitle></CardHeader>
                <CardContent>
                    <div className="flex space-x-2 mb-4">
                        <Input 
                            placeholder="Buscar por nome do arquivo..." 
                            value={searchQuery} 
                            onChange={(e) => setSearchQuery(e.target.value)} 
                        />
                        <Button onClick={handleSearch} disabled={loading}>Buscar</Button>
                    </div>
                    {loading && <p>Carregando...</p>}
                    {error && <p className="text-red-500">{error}</p>}
                    {searchResults.length > 0 && (
                        <ul className="space-y-2 mt-4">
                            {searchResults.map(file => (
                                <li key={file.id} className="border p-2 rounded-md flex justify-between items-center">
                                    <span>{file.name} ({file.mime_type})</span>
                                    <div>
                                        <Button variant="link" onClick={() => window.open(file.web_view_link, '_blank')}>Ver</Button>
                                        <Button variant="link" onClick={() => handleGetFileContent(file.id)}>Ver Conteúdo</Button>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    )}
                    {fileContent && (
                        <Card className="mt-4">
                            <CardHeader><CardTitle>Conteúdo do Arquivo: {fileContent.file_name}</CardTitle></CardHeader>
                            <CardContent>
                                <pre className="whitespace-pre-wrap text-sm border p-2 rounded-md bg-gray-50 dark:bg-gray-800">
                                    {fileContent.content}
                                </pre>
                            </CardContent>
                        </Card>
                    )}
                </CardContent>
            </Card>

            <Card>
                <CardHeader><CardTitle>Google Drive - Criar Novo Arquivo</CardTitle></CardHeader>
                <CardContent>
                    <form onSubmit={handleCreateFile} className="space-y-4">
                        <div>
                            <Label htmlFor="fileName">Nome do Arquivo:</Label>
                            <Input id="fileName" name="name" value={createFileData.name} onChange={handleCreateFileChange} required />
                        </div>
                        <div>
                            <Label htmlFor="mimeType">Tipo MIME (ex: text/plain, application/pdf):</Label>
                            <Input id="mimeType" name="mimeType" value={createFileData.mimeType} onChange={handleCreateFileChange} required />
                        </div>
                        <div>
                            <Label htmlFor="content">Conteúdo (Opcional):</Label>
                            <Textarea id="content" name="content" value={createFileData.content} onChange={handleCreateFileChange} rows="5" />
                        </div>
                        <Button type="submit" disabled={loading}>Criar Arquivo</Button>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
};

export default DrivePage;