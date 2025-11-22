from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr


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
