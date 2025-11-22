from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session

from ..database import engine, Base, getDatabase
from .repository import ExperienciaRepository
from .schema import ExperienciaBase
from ..models import Experiencia


Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/experiencias",
    tags=["experiencias"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{id_candidato}")
async def getExperienciasByCandidatoId(
    id_candidato: int, database: Session = Depends(getDatabase)
):
    experiencias = ExperienciaRepository.getExperienciasByCandidatoId(
        id_candidato, database
    )
    if not experiencias:
        raise HTTPException(status_code=404, detail="Experiências não encontradas")
    return experiencias


@router.post("/{id_candidato}")
async def createExperienciaByCandidatoId(
    id_candidato: int,
    experiencia_data: ExperienciaBase,
    database: Session = Depends(getDatabase),
):
    experiencias = ExperienciaRepository.createExperiencia(
        Experiencia(id_usuario=id_candidato, **experiencia_data.model_dump()), database
    )
    if not experiencias:
        raise HTTPException(status_code=404, detail="Experiências não encontradas")
    return experiencias


@router.delete("/{id_candidato}/{id_experiencia}")
async def deleteExperienciaById(
    id_experiencia: int, database: Session = Depends(getDatabase)
):
    experiencia = ExperienciaRepository.getExperienciaById(id_experiencia, database)
    if not experiencia:
        raise HTTPException(status_code=404, detail="Experiência não encontrada")
    success = ExperienciaRepository.deleteExperiencia(experiencia, database)
    if not success:
        raise HTTPException(status_code=404, detail="Erro ao deletar experiência")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id_candidato}/{id_experiencia}")
async def updateExperienciaById(
    id_experiencia: int,
    experiencia_data: ExperienciaBase,
    database: Session = Depends(getDatabase),
):
    experiencia = ExperienciaRepository.getExperienciaById(id_experiencia, database)
    if experiencia:
        updated_experiencia = ExperienciaRepository.updateExperiencia(
            Experiencia(id_experiencia=id_experiencia, **experiencia_data.model_dump()),
            database,
        )
        return updated_experiencia
