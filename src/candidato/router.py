from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session

from ..database import engine, Base, getDatabase
from .repository import CandidatoRepository
from .schema import CandidatoBase
from ..models import Candidato

Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix = "/candidatos",
    tags = ["candidatos"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def getCandidatos(database: Session = Depends(getDatabase)):
    candidatos = CandidatoRepository.getAllCandidatos(database)
    return candidatos

@router.get("/{id_candidato}")
async def getCandidatoById(id_candidato: int, database: Session = Depends(getDatabase)):
    candidato = CandidatoRepository.getCandidatoById(id_candidato, database)
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato não encontrado")
    return candidato

@router.post("/")
async def createCandidato(new_candidato: CandidatoBase, database: Session = Depends(getDatabase)):
    candidato_already_exists = CandidatoRepository.candidatoExistsByEmail(new_candidato.email, database)
    if candidato_already_exists:
        raise HTTPException(
                status_code=400,
                detail="Email already registered"
        )
    else:
        new_candidato = CandidatoRepository.createCandidato(Candidato(**new_candidato.model_dump()), database)
        return new_candidato

@router.put("/{id_candidato}")
async def updateCandidatoById(id_candidato: int, candidato_data: CandidatoBase, database: Session = Depends(getDatabase)):
    candidato = CandidatoRepository.getCandidatoById(id_candidato, database)
    if candidato:
        updated_candidato = CandidatoRepository.updateCandidato(Candidato(id_usuario = id_candidato, **candidato_data.model_dump()), database)
        return updated_candidato

@router.delete("/{id_candidato}")
async def deleteCandidato(id_candidato: int, database: Session = Depends(getDatabase)):
    candidato = CandidatoRepository.getCandidatoById(id_candidato, database)
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato não encontrado")
    success = CandidatoRepository.deleteCandidato(candidato, database)
    if not success:
        raise HTTPException(status_code=500, detail="Erro ao deletar candidato")
    return Response(status_code = status.HTTP_204_NO_CONTENT)