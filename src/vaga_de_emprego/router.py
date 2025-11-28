from fastapi import APIRouter, HTTPException, Depends, Query, Response, status
from sqlalchemy.orm import Session

from ..auth.repository import requireAdminGestor, requireGestor

from ..database import engine, Base, getDatabase
from .repository import VagaDeEmpregoRepository
from .schema import VagaDeEmpregoBase, VagaDeEmpregoResponse
from ..models import Gestor, Usuario, VagaDeEmprego

from ..candidatura.repository import CandidaturaRepository

Base.metadata.create_all(bind=engine)

router = APIRouter(
	prefix='/vagas_de_emprego',
	tags=['vagas de emprego'],
	responses={404: {'description': 'Not found'}},
)


@router.get('/')
async def getVagasDeEmprego(database: Session = Depends(getDatabase)):
	vagas_de_emprego = VagaDeEmpregoRepository.getAllVagasDeEmprego(database)
	return vagas_de_emprego


@router.get('_com_empresas')
async def getVagasDeEmpregoWithEmpresas(database: Session = Depends(getDatabase)):
	vagas_de_emprego = VagaDeEmpregoRepository.getAllVagasDeEmpregoComEmpresas(database)
	return vagas_de_emprego


@router.get('/{id_vaga_de_emprego}')
async def getVagaDeEmpregoById(
	id_vaga_de_emprego: int, database: Session = Depends(getDatabase)
):
	vagas_de_emprego = VagaDeEmpregoRepository.getVagaDeEmpregoWithEmpresaById(
		id_vaga_de_emprego, database
	)
	return vagas_de_emprego


@router.get('/empresa/{id_empresa}')
async def getVagasDeEmpregoByEmpresaId(
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


@router.post(
	'/', response_model=VagaDeEmpregoResponse, status_code=status.HTTP_201_CREATED
)
async def createVagaDeEmprego(
	vaga_de_emprego_data: VagaDeEmpregoBase,
	database: Session = Depends(getDatabase),
	current_gestor: Gestor = Depends(requireGestor),
):
	new_vaga_de_emprego = VagaDeEmpregoRepository.createVagaDeEmprego(
		VagaDeEmprego(**vaga_de_emprego_data.model_dump()), database
	)
	return new_vaga_de_emprego


@router.delete('/{id_vaga_de_emprego}')
async def deleteVagaDeEmpregoById(
	id_vaga_de_emprego: int,
	database: Session = Depends(getDatabase),
	current_user: Usuario = Depends(requireAdminGestor),
):
	vaga_de_emprego = VagaDeEmpregoRepository.getVagaDeEmpregoById(
		id_vaga_de_emprego, database
	)
	if not vaga_de_emprego:
		raise HTTPException(status_code=404, detail='Vaga de emprego não encontrado')
	success = VagaDeEmpregoRepository.deleteVagaDeEmprego(vaga_de_emprego, database)
	if not success:
		raise HTTPException(status_code=500, detail='Erro ao deletar vaga de emprego')
	return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id_vaga_de_emprego}')
async def updateVagaDeEmpregoById(
	id_vaga_de_emprego: int,
	vaga_de_emprego_data: VagaDeEmpregoBase,
	database: Session = Depends(getDatabase),
	current_user: Usuario = Depends(requireAdminGestor),
):
	vaga_de_emprego = VagaDeEmpregoRepository.getVagaDeEmpregoById(
		id_vaga_de_emprego, database
	)
	if vaga_de_emprego:
		updated_vaga_de_emprego = VagaDeEmpregoRepository.updateVagaDeEmprego(
			VagaDeEmprego(
				id_vaga_de_emprego=id_vaga_de_emprego,
				**vaga_de_emprego_data.model_dump(),
			),
			database,
		)
		return updated_vaga_de_emprego


@router.get('/{id_vaga_de_emprego}/candidaturas')
async def getVagaDeEmpregosCandidaturas(
	id_vaga_de_emprego: int, database: Session = Depends(getDatabase)
):
	candidaturas = CandidaturaRepository.getCandidaturasWithCandidatoByVagaDeEmpregoId(
		id_vaga_de_emprego, database
	)
	return candidaturas
