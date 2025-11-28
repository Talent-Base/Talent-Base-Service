from typing import Optional
from pydantic import BaseModel


class CandidatoBase(BaseModel):
	id_candidato: int
	nome: str
	email: str
	titulo_profissional: Optional[str] = None
	estado: Optional[str] = None
	cidade: Optional[str] = None
	resumo: Optional[str] = None
	situacao_empregaticia: Optional[str] = None


class CandidatoResponse(CandidatoBase):
	id_candidato: int
