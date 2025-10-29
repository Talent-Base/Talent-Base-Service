from typing import Optional
from pydantic import BaseModel

class ExperienciaBase(BaseModel):
    nome_instituicao: str
    cargo: str
    periodo_experiencia: int
    descricao: Optional[str] = None
    nome_curso: Optional[str] = None
    grau_obtido: Optional[str] = None

class ExperienciaResponse(ExperienciaBase):
    id: int