import httpx
from ..core.config import settings

class YouTrackService:
    """
    Serviço para interagir com a API REST do YouTrack.
    As credenciais são carregadas diretamente das configurações do ambiente.
    """
    def __init__(self):
        """
        Inicializa o serviço com a URL base e os headers de autenticação.
        """
        self.base_url = settings.YOUTRACK_BASE_URL
        # Garante que a URL base termine com uma barra
        if not self.base_url.endswith('/'):
            self.base_url += '/'
            
        self.headers = {
            "Authorization": f"Bearer {settings.YOUTRACK_API_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        print("YouTrack Service Initialized.")

    async def _make_request(self, method: str, endpoint: str, params: dict = None) -> dict:
        """
        Método auxiliar para realizar chamadas à API do YouTrack.
        """
        url = f"{self.base_url}api/{endpoint}"
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.request(method, url, headers=self.headers, params=params)
                response.raise_for_status()  # Lança uma exceção para respostas com erro (4xx ou 5xx)
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"Erro na API do YouTrack: {e.response.status_code} - {e.response.text}")
            except httpx.RequestError as e:
                print(f"Não foi possível conectar ao YouTrack. Verifique a URL e a conexão: {e}")
            except Exception as e:
                print(f"Ocorreu um erro inesperado no serviço do YouTrack: {e}")
        return {}

    async def get_pending_tasks_count(self) -> int:
        """
        Busca o número total de tarefas (issues) que não estão em um estado final (Resolvida, Fechada, etc.).
        """
        print("Buscando contagem de tarefas pendentes no YouTrack...")
        # A query busca por issues que não tenham um estado "Resolved"
        # O '$top=0' é uma otimização para apenas obter a contagem total no campo 'total'
        params = {
            "query": "State: -Resolved",
            "$top": 0 
        }
        data = await self._make_request("GET", "issues", params=params)
        # O número total de issues que correspondem à query fica no campo 'total'
        count = data.get("total", 0)
        print(f"Encontradas {count} tarefas pendentes.")
        return count

    async def get_active_projects_count(self) -> int:
        """
        Busca o número de projetos que não estão arquivados.
        """
        print("Buscando contagem de projetos ativos no YouTrack...")
        params = {
            "fields": "id,archived", # Pede apenas os campos 'id' e 'archived'
            "$top": -1 # Pede todos os projetos
        }
        projects = await self._make_request("GET", "admin/projects", params=params)
        
        if not isinstance(projects, list):
            return 0
            
        # Filtra a lista para contar apenas os projetos que não estão arquivados
        active_projects = [p for p in projects if not p.get("archived", False)]
        count = len(active_projects)
        print(f"Encontrados {count} projetos ativos.")
        return count

# Cria uma instância única do serviço para ser usada em toda a aplicação
youtrack_service = YouTrackService()