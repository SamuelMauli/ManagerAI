from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..database import get_db
from ..services import google
from ..utils.security import create_access_token, get_current_user

router = APIRouter()

@router.post("/google", response_model=schemas.Token)
def auth_google(code_container: dict, db: Session = Depends(get_db)):
    code = code_container.get("code")
    print(f"--- PASSO 1: Recebido código de autorização do frontend: {code[:30]}... ---")

    if not code:
        print("!!! ERRO: Nenhum código recebido.")
        raise HTTPException(status_code=400, detail="Authorization code not found")

    print("--- PASSO 2: Trocando o código por informações do usuário no Google... ---")
    user_info_tuple = google.exchange_code_for_user_info(code)
    
    if not user_info_tuple:
        print("!!! ERRO: Falha ao obter informações do usuário do Google. Verifique se as APIs (Gmail, People, Calendar) estão ativadas no Google Cloud.")
        raise HTTPException(status_code=400, detail="Could not retrieve user info from Google")
    
    user_info, credentials = user_info_tuple
    print(f"--- PASSO 3: Informações do usuário recebidas do Google: {user_info} ---")
    print(f"--- Credenciais (token): {credentials.token[:30]}... ---")

    print("--- PASSO 4: Verificando se o usuário existe ou criando um novo no banco de dados... ---")
    user = crud.get_or_create_user(db, google_info=user_info, credentials=credentials)

    if not user:
        print("!!! ERRO: Falha ao criar ou buscar o usuário no banco de dados.")
        raise HTTPException(status_code=500, detail="Could not create or retrieve user")
    
    print(f"--- PASSO 5: Usuário '{user.email}' processado com sucesso. Gerando token JWT... ---")
    access_token = create_access_token(data={"sub": user.email})
    
    print("--- PASSO 6: Token JWT gerado. Enviando para o frontend. ---")
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

# ... (resto do arquivo sem alterações)
@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.email)
    if not user or not user.hashed_password or not crud.pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}