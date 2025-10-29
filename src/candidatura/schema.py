from datetime import datetime

from pydantic import BaseModel

class CandidaturaBase(BaseModel):
    id_candidato: int
    id_vaga_de_emprego: int
    status: {"Em análise", "Aprovado", "Rejeitado"}
    data: datetime

class CandidaturaResponse(CandidaturaBase):
    id_candidatura: int
