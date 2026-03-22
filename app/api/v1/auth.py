from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import JWTError, jwt
from app.db.session import get_db
from app.core.config import settings
from app.core import security
from app.schemas.schemas import Token, UserCreate, UserUpdate, UserResponse, TokenData
from app.repository.repository import UserRepository
from app.models.models import User
from typing import List

router = APIRouter(prefix="/auth", tags=["Autenticação"])
# bearer_scheme permite colar o token diretamente (mais intuitivo para alguns usuários)
bearer_scheme = HTTPBearer()

async def get_current_user(
    db: Session = Depends(get_db), 
    token: HTTPBearer = Depends(bearer_scheme)
):
    # Nota: Usamos HTTPBearer para que no Swagger apareça o campo de token.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=UserResponse, summary="Registrar novo usuário")
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    return user_repo.create(user_in)

@router.post("/login", response_model=Token, summary="Login do usuário")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token = security.create_refresh_token(data={"sub": user.email})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh", response_model=Token, summary="Renovar token de acesso")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar o refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(email=email)
    if user is None:
        raise credentials_exception
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    # Opcionalmente podemos rotacionar o refresh token aqui também
    new_refresh_token = security.create_refresh_token(data={"sub": user.email})
    
    return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}

@router.get("/users", response_model=List[UserResponse], summary="Listar todos os usuários")
def get_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_repo = UserRepository(db)
    return user_repo.get_all(skip=skip, limit=limit)

@router.get("/users/{user_id}", response_model=UserResponse, summary="Obter usuário por ID")
def get_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

@router.put("/users/{user_id}", response_model=UserResponse, summary="Atualizar usuário")
def update_user(
    user_id: int, 
    user_in: UserUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Opcional: Impedir que um usuário altere o e-mail para um já existente (se alterado)
    if user_in.email and user_in.email != user.email:
        existing_user = user_repo.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="E-mail já cadastrado por outro usuário")
            
    return user_repo.update(user_id, user_in)

@router.delete("/users/{user_id}", summary="Excluir usuário")
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_repo = UserRepository(db)
    if not user_repo.delete(user_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"message": "Usuário excluído com sucesso"}
