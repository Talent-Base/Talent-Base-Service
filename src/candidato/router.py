from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session

from ..auth.repository import requireAdmin, requireCandidato

from ..database import engine, Base, getDatabase
from .repository import CandidatoRepository
from .schema import CandidatoBase
from ..models import Candidato, Notificacao, Usuario

Base.metadata.create_all(bind=engine)

router = APIRouter(
	prefix='/candidatos',
	tags=['candidatos'],
	responses={404: {'description': 'Not found'}},
)


@router.get('/')
async def getCandidatos(database: Session = Depends(getDatabase)):
	candidatos = CandidatoRepository.getAllCandidatos(database)
	return candidatos


@router.get('/{id_candidato}/stats')
async def getStatisticsByCandidatoId(
	id_candidato: int,
	database: Session = Depends(getDatabase),
	current_candidato: Candidato = Depends(requireCandidato),
):
	statistics = CandidatoRepository.getStatisticsByCandidatoId(id_candidato, database)
	return statistics


@router.get('/{id_candidato}')
async def getCandidatoById(id_candidato: int, database: Session = Depends(getDatabase)):
	candidato = CandidatoRepository.getCandidatoById(id_candidato, database)
	if not candidato:
		raise HTTPException(status_code=404, detail='Candidato não encontrado')
	return candidato


@router.post('/')
async def createCandidato(
	new_candidato: CandidatoBase, database: Session = Depends(getDatabase)
):
	candidato_already_exists = CandidatoRepository.candidatoExistsByEmail(
		new_candidato.email, database
	)
	if candidato_already_exists:
		raise HTTPException(status_code=400, detail='Email already registered')
	else:
		new_candidato = CandidatoRepository.createCandidato(
			Candidato(**new_candidato.model_dump()), database
		)
		return new_candidato


@router.put('/{id_candidato}')
async def updateCandidatoById(
	id_candidato: int,
	candidato_data: CandidatoBase,
	database: Session = Depends(getDatabase),
	current_candidato: Candidato = Depends(requireCandidato),
):
	if id_candidato != current_candidato.id:
		raise HTTPException(
			status_code=403, detail='Você não pode editar outro usuário.'
		)
	candidato = CandidatoRepository.getCandidatoById(id_candidato, database)
	if not candidato:
		raise HTTPException(status_code=404, detail='Candidato não encontrado')
	updated_candidato = CandidatoRepository.updateCandidato(
		Candidato(**candidato_data.model_dump()),
		database,
	)
	return updated_candidato


@router.delete('/{id_candidato}')
async def deleteCandidatoById(
	id_candidato: int,
	database: Session = Depends(getDatabase),
	current_admin: Usuario = Depends(requireAdmin),
):
	candidato = CandidatoRepository.getCandidatoById(id_candidato, database)
	if not candidato:
		raise HTTPException(status_code=404, detail='Candidato não encontrado')
	success = CandidatoRepository.deleteCandidato(candidato, database)
	if not success:
		raise HTTPException(status_code=500, detail='Erro ao deletar candidato')
	return Response(status_code=status.HTTP_204_NO_CONTENT)


