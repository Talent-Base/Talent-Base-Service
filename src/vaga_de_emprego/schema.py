from typing import Optional
from datetime import date
from decimal import Decimal

from pydantic import BaseModel

class VagaDeEmpregoBase(BaseModel):
    nome: str
    empresa: int
    data: date
    estado: str
    cidade: str
    salario: Decimal
    cargo: str
    nivel: {"Junior", "Pleno", "Senior", "Executivo"}
    tipo_contrato: {"CLT", "Estagio"}
    modalidade: {"Presencial", "Hibrido", "Remoto"}
    descricao: Optional[str] = None

class VagaDeEmpregoResponse(VagaDeEmpregoBase):
    id_vaga_de_emprego: int

