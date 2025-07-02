from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from jose import jwt
from datetime import datetime, timedelta, timezone


from fastapi import Header, Depends
from typing import Annotated
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
# Importa as configurações validadas do arquivo config.py
from .config import settings

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TokenRequest(BaseModel):
    code: str

@app.post("/auth/google/callback")
async def auth_google_callback(token_request: TokenRequest):
    code = token_request.code
    print("1. Backend recebeu o código de autorização.")

    token_url = "https://oauth2.googleapis.com/token"
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost:5173", # O redirect_uri aqui deve ser a origem da chamada
    }

    try:
        async with httpx.AsyncClient() as client:
            print("2. Trocando o código pelo token de acesso com a Google...")
            response = await client.post(token_url, data=params)
            
            # Força o levantamento de uma exceção se a resposta não for 2xx
            response.raise_for_status() 
            
            token_data = response.json()
            access_token = token_data.get("access_token")
            print("3. Token de acesso recebido da Google com sucesso.")

            print("4. Buscando informações do usuário...")
            user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
            headers = {"Authorization": f"Bearer {access_token}"}
            user_response = await client.get(user_info_url, headers=headers)
            user_response.raise_for_status()
            
            user_info = user_response.json()
            email = user_info.get("email")
            print(f"5. Informações do usuário recebidas para: {email}")

        # AQUI: Adicione sua lógica de banco de dados (criar ou buscar usuário)

        print("6. Criando token JWT interno para o frontend...")
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        jwt_payload = {
            "sub": email,
            "exp": expire
        }
        
        token = jwt.encode(jwt_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        print("7. Token JWT criado. Enviando para o frontend.")

        return {"access_token": token, "token_type": "bearer"}

    except httpx.HTTPStatusError as e:
        # Erro na comunicação com a API do Google
        print(f"[ERRO] Falha na chamada à Google: {e.response.status_code}")
        print(f"[ERRO] Resposta da Google: {e.response.text}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Falha ao validar com o Google: {e.response.json().get('error_description', 'Erro desconhecido')}"
        )
    except Exception as e:
        # Outros erros inesperados
        print(f"[ERRO] Um erro inesperado ocorreu: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno no servidor."
        )

# Rota de teste para verificar se o servidor está no ar
@app.get("/")
def read_root():
    return {"status": "Backend is running"}

@app.get("/emails/unread")
async def get_unread_emails(token: str): # Receber o token como parâmetro
    try:
        # AQUI: O ideal seria descriptografar um token JWT seguro
        # Por simplicidade agora, vamos assumir que o token é o de acesso
        # Esta parte precisará ser mais robusta no futuro
        creds = Credentials(token=token) # Simplificação perigosa para agora
        
        service = build('gmail', 'v1', credentials=creds)
        
        # Busca por mensagens não lidas na caixa de entrada
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
        messages = results.get('messages', [])

        email_list = []
        if not messages:
            return {"emails": []}
            
        # Pega apenas os 5 primeiros e-mails para não sobrecarregar
        for message in messages[:5]:
            msg = service.users().messages().get(userId='me', id=message['id'], format='metadata', metadataHeaders=['From', 'Subject', 'Date']).execute()
            payload = msg.get('payload', {})
            headers = payload.get('headers', [])
            
            email_data = {
                "id": msg.get('id'),
                "snippet": msg.get('snippet', '').strip()
            }

            for header in headers:
                if header['name'] == 'From':
                    email_data['from'] = header['value']
                if header['name'] == 'Subject':
                    email_data['subject'] = header['value']
                if header['name'] == 'Date':
                    email_data['date'] = header['value']
            
            email_list.append(email_data)

        return {"emails": email_list}

    except Exception as e:
        # Log do erro no servidor para depuração
        print(f"[ERRO GMAIL]: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível buscar os e-mails. Pode ser necessário refazer o login."
        )
    
@app.get("/emails/unread")
async def get_unread_emails(authorization: Annotated[str, Header()]):
    """
    Busca e-mails não lidos esperando um token no cabeçalho 'Authorization: Bearer <token>'.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Cabeçalho de autorização inválido")

    token = authorization.split("Bearer ")[1]
    
    try:
        # Usamos o token de acesso do Google diretamente
        creds = Credentials(token=token)
        service = build('gmail', 'v1', credentials=creds)
        
        results = service.users().messages().list(
            userId='me', labelIds=['INBOX'], q="is:unread", maxResults=10
        ).execute()
        
        messages = results.get('messages', [])
        if not messages:
            return {"emails": []}

        email_list = []
        for message in messages:
            msg = service.users().messages().get(
                userId='me', id=message['id'], format='metadata', metadataHeaders=['From', 'Subject', 'Date']
            ).execute()
            
            headers = msg.get('payload', {}).get('headers', [])
            email_data = {
                "id": msg.get('id'),
                "snippet": msg.get('snippet', '').strip(),
                "from": next((h['value'] for h in headers if h['name'] == 'From'), 'N/A'),
                "subject": next((h['value'] for h in headers if h['name'] == 'Subject'), 'Sem Assunto'),
            }
            email_list.append(email_data)

        return {"emails": email_list}

    except Exception as e:
        print(f"[ERRO GMAIL]: {e}")
        raise HTTPException(
            status_code=400,
            detail="Não foi possível buscar os e-mails. O token pode ter expirado."
        )