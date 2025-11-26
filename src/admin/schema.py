from pydantic import BaseModel


class StatsBase(BaseModel):
    usuarios_totais: int
    candidatos_totais: int
    empresas_totais: int
    vagas_totais: int
    candidaturas_totais: int


class ToggleStatusRequest(BaseModel):
    new_status: bool
