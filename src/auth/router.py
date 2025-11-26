from datetime import timedelta
import os

from fastapi import APIRouter, Body, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from jwt import InvalidTokenError
import jwt
from sqlalchemy.orm import Session

from src.models import Usuario
from src.usuario.repository import UsuarioRepository
from src.usuario.schema import AuthResponse, UsuarioResponse

from ..database import engine, Base, getDatabase
from .repository import (
    authenticateUser,
    createAccessToken,
    createRefreshToken,
    getCurrentActiveUser,
)
from .schema import Token

SECRET_KEY = os.getenv(
    "SECRET_KEY", "3451923f1a545ea6fe648d5a2ff6eca91a5522d9652d742df632779c8a75c8ce"
)
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)

Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login", response_model=AuthResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    database: Session = Depends(getDatabase),
):
    user = authenticateUser(form_data.username, form_data.password, database)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sua conta foi desativada. Entre em contato com o suporte."
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = createAccessToken(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token = createRefreshToken({"sub": user.email})
    usuario = UsuarioRepository.getUsuarioByEmail(user.email, database)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": UsuarioResponse.model_validate(usuario),
    }


@router.get("/me", response_model=UsuarioResponse)
async def get_me(current_user: Usuario = Depends(getCurrentActiveUser)):
    return current_user


@router.post("/refresh")
def refresh_token(
    refresh_token: str = Body(...), database: Session = Depends(getDatabase)
):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Carregar o usuário
    user = UsuarioRepository.getUsuarioByEmail(username, database)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    # Criar novo access token
    new_access_token = createAccessToken({"sub": username})

    return {"access_token": new_access_token}
