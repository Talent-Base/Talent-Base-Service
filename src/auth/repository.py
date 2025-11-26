from datetime import datetime, timedelta, timezone
import os

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..database import getDatabase
from ..security import verifyPassword
from .schema import TokenData
from ..usuario.repository import UsuarioRepository
from ..models import Usuario

SECRET_KEY = os.getenv(
    "SECRET_KEY", "3451923f1a545ea6fe648d5a2ff6eca91a5522d9652d742df632779c8a75c8ce"
)
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 30)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def createAccessToken(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def createRefreshToken(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})

    refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return refresh_token


def authenticateUser(
    username: str, senha: str, database: Session = Depends(getDatabase)
):
    user = UsuarioRepository.getUsuarioByEmail(username, database)
    if not user:
        return False
    if not verifyPassword(senha, user.senha):
        return False
    return user


async def getCurrentUser(
    token: str = Depends(oauth2_scheme), database: Session = Depends(getDatabase)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = UsuarioRepository.getUsuarioByEmail(token_data.username, database)
    if user is None:
        raise credentials_exception
    return user


async def getCurrentActiveUser(current_user: Usuario = Depends(getCurrentUser)):
    if not current_user.ativo:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def requireCandidato(user: Usuario = Depends(getCurrentActiveUser)):
    if user.papel != "candidato":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas candidatos podem acessar esta rota.",
        )
    return user


def requireGestor(user: Usuario = Depends(getCurrentActiveUser)):
    if user.papel != "gestor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas gestores podem acessar esta rota.",
        )
    return user


def requireAdmin(user: Usuario = Depends(getCurrentActiveUser)):
    if user.papel != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas admins podem acessar esta rota.",
        )
    return user
