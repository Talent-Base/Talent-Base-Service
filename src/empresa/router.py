from fastapi import APIRouter, HTTPException, Depends, Query, Response, status
from sqlalchemy.orm import Session

from ..auth.repository import requireGestor

from ..database import engine, Base, getDatabase
from .repository import EmpresaRepository
from .schema import EmpresaBase
from ..models import Empresa, Usuario

from ..vaga_de_emprego.repository import VagaDeEmpregoRepository
from ..gestor.repository import GestorRepository

Base.metadata.create_all(bind=engine)

router = APIRouter(
	prefix='/empresas',
	tags=['empresas'],
	responses={404: {'description': 'Not found'}},
)


@router.get('/')
async def getEmpresas(database: Session = Depends(getDatabase)):
	empresas = EmpresaRepository.getAllEmpresas(database)
	return empresas


@router.get('/{id_empresa}')
async def getEmpresaById(id_empresa: int, database: Session = Depends(getDatabase)):
	empresa = EmpresaRepository.getEmpresaById(id_empresa, database)
	if not empresa:
		raise HTTPException(status_code=404, detail='Empresa não encontrada')
	return empresa


@router.get('/{id_empresa}/stats')
async def getStatisticsByEmpresaId(
	id_empresa: int,
	database: Session = Depends(getDatabase),
	current_user: Usuario = Depends(requireGestor),
):
	statistics = EmpresaRepository.getStatisticsByEmpresaId(id_empresa, database)
	return statistics


@router.post('/')
async def createEmpresa(
	empresa_data: EmpresaBase, database: Session = Depends(getDatabase)
):
	empresa_already_exists = EmpresaRepository.empresaAlredyExists(
		empresa_data.cnpj, empresa_data.nome_empresa, database
	)
	if empresa_already_exists:
		raise HTTPException(status_code=400, detail='Empresa already registered')
	else:
		new_empresa = EmpresaRepository.createEmpresa(
			Empresa(**empresa_data.model_dump()), database
		)
		return new_empresa


@router.delete('/{id_empresa}')
async def deleteEmpresaById(id_empresa: int, database: Session = Depends(getDatabase)):
	empresa = EmpresaRepository.getEmpresaById(id_empresa, database)
	if not empresa:
		raise HTTPException(status_code=404, detail='Empresa não encontrada')
	success = EmpresaRepository.deleteEmpresa(empresa, database)
	if not success:
		raise HTTPException(status_code=500, detail='Erro ao deletar empresa')
	return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id_empresa}')
async def updateEmpresaById(
	id_empresa: int,
	empresa_data: EmpresaBase,
	database: Session = Depends(getDatabase),
	current_user: Usuario = Depends(requireGestor),
):
	empresa = EmpresaRepository.getEmpresaById(id_empresa, database)
	if not empresa:
		raise HTTPException(status_code=404, detail='Empresa não encontrada')
	updated_empresa = EmpresaRepository.updateEmpresa(
		Empresa(id_empresa=id_empresa, **empresa_data.model_dump()), database
	)
	return updated_empresa


@router.get('/{id_empresa}/vagas_de_emprego')
async def getEmpresasVagaDeEmprego(
	id_empresa: int,
	database: Session = Depends(getDatabase),
	limit: int = Query(None, ge=1, le=5),
):
	if limit:
		vagas_de_emprego = VagaDeEmpregoRepository.getVagaDeEmpregoByEmpresaId(
			id_empresa, database, limit
		)
	else:
		vagas_de_emprego = VagaDeEmpregoRepository.getVagaDeEmpregoByEmpresaId(
			id_empresa, database
		)
	return vagas_de_emprego


@router.get('{id_empresa}/getores')
async def getEmpresasGestores(
	id_empresa: int, database: Session = Depends(getDatabase)
):
	gestores = GestorRepository.getGestoresByEmpresaId(id_empresa, database)
	if not gestores:
		raise HTTPException(status_code=404, detail='Gestores não encontradas')
	return gestores
