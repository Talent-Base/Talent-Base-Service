from datetime import date
from typing import Optional
from pydantic import BaseModel


class NotificacaoBase(BaseModel):
    titulo: str
    mensagem: str
    id_candidato: int
    id_candidatura: Optional[int] = None
    id_vaga_de_emprego: Optional[int] = None
    visualizada: bool = False


class NotificacaoResponse(NotificacaoBase):
    id: int
    date: date
