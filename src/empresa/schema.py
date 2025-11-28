from typing import Optional
from pydantic import BaseModel


class EmpresaBase(BaseModel):
	nome_empresa: str
	cnpj: str
	cidade: str
	estado: str
	email_contato: Optional[str] = None
	descricao: Optional[str] = None


class EmpresaResponse(EmpresaBase):
	id_empresa: int
