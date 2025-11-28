from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from src.vaga_de_emprego.schema import VagaDeEmpregoBase


class Status(str, Enum):
	PENDENTE = 'Pendente'
	ANALISE = 'Em análise'
	ACEITO = 'Aceito'
	REJEITADO = 'Rejeitado'


class CandidaturaBase(BaseModel):
	id_candidato: int
	id_vaga_de_emprego: int
	status: Status = Field(default='Pendente')
	data: datetime
	data_atualizacao: Optional[datetime] = None

	model_config = {'from_attributes': True}


class CandidaturaUpdate(BaseModel):
	status: Status
	data_atualizacao: datetime


class CandidaturaResponse(CandidaturaBase):
	id_candidatura: int


class CandidaturaWithVagaResponse(CandidaturaResponse):
	vaga_de_emprego: VagaDeEmpregoBase

	model_config = {'from_attributes': True}
