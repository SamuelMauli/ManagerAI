
import sys
import os
from urllib.parse import unquote  # <--- BIBLIOTECA ADICIONADA
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

# --- Configurações (não precisam ser alteradas) ---
CLIENT_ID = "800219743675-r22opm2dfp1o4k6c0sqcs2r8umdp0h0m.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:5173"
SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']

def main():
    if len(sys.argv) < 2:
        print("ERRO: Faltou o código de autorização.")
        return

    # --- CORREÇÃO APLICADA AQUI ---
    # Decodifica o código para transformar caracteres como %2F em /
    auth_code_encoded = sys.argv[1]
    auth_code_decoded = unquote(auth_code_encoded)
    print(f">>> Código recebido (codificado): {auth_code_encoded}")
    print(f">>> Código a ser usado (decodificado): {auth_code_decoded}\n")
    # --- FIM DA CORREÇÃO ---

    try:
        client_config = {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        }

        flow = Flow.from_client_config(
            client_config=client_config,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )

        print(">>> Passo 1: Tentando trocar o código por um token...")
        flow.fetch_token(code=auth_code_decoded) # Usa o código decodificado
        credentials = flow.credentials
        print(">>> SUCESSO! Token recebido.")

        print("\n>>> Passo 2: Usando o token para buscar informações do usuário...")
        service = build('oauth2', 'v2', credentials=credentials)
        user_info = service.userinfo().get().execute()
        print(">>> SUCESSO! Informações recebidas.")

        print("\n--- ✅ VALIDAÇÃO CONCLUÍDA COM SUCESSO ✅ ---")
        print(f"  Email: {user_info.get('email')}")
        print(f"  Nome: {user_info.get('name')}")
        print("---------------------------------------------")

    except Exception as e:
        print(f"\n--- ❌ FALHA NA VALIDAÇÃO ❌ ---\nOcorreu um erro: {e}")

if __name__ == "__main__":
    main()
