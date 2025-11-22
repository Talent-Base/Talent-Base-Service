from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Status(str, Enum):
    ANALISE = "Em análise"
    APROVADO = "Aprovado"
    REJEITADO = "Rejeitado"


class CandidaturaBase(BaseModel):
    id_candidato: int
    id_vaga_de_emprego: int
    status: Status
    data: datetime


class CandidaturaResponse(CandidaturaBase):
    id_candidatura: int
