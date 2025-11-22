from typing import Optional
from pydantic import BaseModel


class GestorBase(BaseModel):
    nome: str
    email: str
    id_empresa: Optional[int] = None


class GestorResponse(GestorBase):
    id_gestor: int
