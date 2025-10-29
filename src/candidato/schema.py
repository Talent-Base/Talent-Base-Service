from typing import Optional
from pydantic import BaseModel

class CandidatoBase(BaseModel):
    nome: str
    email: str
    estado: Optional[str] = None
    cidade: Optional[str] = None
    resumo: Optional[str] = None
    situacao_empregaticia: Optional[str] = None

class CandidatoResponse(CandidatoBase):
    id: int