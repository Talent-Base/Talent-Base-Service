from fastapi import APIRouter, HTTPException, Depends, Response, status
from sqlalchemy.orm import Session

from ..database import engine, Base, getDatabase
from .repository import CandidaturaRepository
from .schema import CandidaturaBase
from ..models import Candidatura

Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/candidaturas",
    tags=["candidaturas"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def getCandidatura(database: Session = Depends(getDatabase)):
    candidaturas = CandidaturaRepository.getAllCandidaturas(database)
    return candidaturas


@router.get("/{id_candidatura}")
async def getCandidaturaById(
    id_candidatura: int, database: Session = Depends(getDatabase)
):
    candidatura = CandidaturaRepository.getCandidaturaById(id_candidatura, database)
    if candidatura is None:
        raise HTTPException(status_code=404, detail="Candidatura not found")
    return candidatura


@router.post("/")
async def createCandidatura(
    new_candidatura: CandidaturaBase, database: Session = Depends(getDatabase)
):
    candidatura_already_exists = CandidaturaRepository.candidaturaExists(
        new_candidatura.id_candidato, new_candidatura.id_vaga_de_emprego, database
    )
    if candidatura_already_exists:
        raise HTTPException(status_code=400, detail="Candidatura already registered")
    new_candidatura = CandidaturaRepository.createCandidatura(
        Candidatura(**new_candidatura.model_dump()), database
    )
    return new_candidatura


@router.put("/{id_candidatura}")
async def updateCandidaturaStatusById(
    id_candidatura: int,
    candidatura_status: str,
    database: Session = Depends(getDatabase),
):
    candidatura = CandidaturaRepository.getCandidaturaById(id_candidatura, database)
    if not candidatura:
        raise HTTPException(status_code=404, detail="Candidatura não encontrada")
    updated_candidatura = CandidaturaRepository.updateCandidatura(
        Candidatura(
            id_candidatura=id_candidatura,
            **candidatura.model_dump(),
            status=candidatura_status,
        ),
        database,
    )
    return updated_candidatura


@router.delete("/{id_candidatura}")
async def deleteCandidatura(
    id_candidatura: int, database: Session = Depends(getDatabase)
):
    candidatura = CandidaturaRepository.getCandidaturaById(id_candidatura, database)
    if not candidatura:
        raise HTTPException(status_code=404, detail="Candidatura not found")
    success = CandidaturaRepository.deleteCandidatura(candidatura, database)
    if not success:
        raise HTTPException(status_code=500, detail="Erro ao deletar candidatura")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
