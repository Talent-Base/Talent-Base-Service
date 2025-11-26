from typing import Optional
from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel

from ..empresa.schema import EmpresaResponse


class NivelEnum(str, Enum):
    JUNIOR = "Junior"
    SENIOR = "Senior"
    PLENO = "Pleno"
    EXECUTIVO = "Executivo"


class TipoContrato(str, Enum):
    CLT = "CLT"
    ESTAGIO = "Estagio"


class Modalidade(str, Enum):
    PRESENCIAL = "Presencial"
    HIBRIDO = "Híbrido"
    REMOTO = "Remoto"


class VagaDeEmpregoBase(BaseModel):
    nome_vaga_de_emprego: str
    id_empresa: int
    data: date
    estado: str
    cidade: str
    salario: Decimal
    cargo: str
    nivel: NivelEnum
    tipo_contrato: TipoContrato
    modalidade: Modalidade
    descricao: Optional[str] = None


class VagaDeEmpregoResponse(VagaDeEmpregoBase):
    id_vaga_de_emprego: int


class VagaDeEmpregoWithEmpresaResponse(VagaDeEmpregoResponse):
    empresa: EmpresaResponse
