from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr

from src.empresa.schema import EmpresaBase


class Papel(str, Enum):
    candidato = "candidato"
    gestor = "gestor"
    admin = "admin"


class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    papel: Papel


class UsuarioCreate(UsuarioBase):
    senha: str


class UsuarioGestorCreate(UsuarioCreate):
    empresa: EmpresaBase


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    papel: Optional[Papel] = None


class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UsuarioResponse
