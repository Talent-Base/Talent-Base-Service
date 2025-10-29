from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session

from ..database import engine, Base, getDatabase
from .repository import GestorRepository
from .schema import GestorBase
from ..models import Gestor

Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix = "/gestores",
    tags = ["gestores"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def getGestores(database: Session = Depends(getDatabase)):
    gestores = GestorRepository.getAllGestores(database)
    return gestores

@router.get("/{id_gestor}")
async def getGestorById(id_gestor: int, database: Session = Depends(getDatabase)):
    gestor = GestorRepository.getGestorById(id_gestor, database)
    if not gestor:
        raise HTTPException(
            status_code=404, 
            detail="Gestor não encontrado"
        )
    return gestor

@router.post("/")
async def createGestor(new_gestor: GestorBase, database: Session = Depends(getDatabase)):
    gestor_already_exists = GestorRepository.gestorExistsByEmail(new_gestor.email, database)
    if gestor_already_exists:
        raise HTTPException(
                status_code=400,
                detail="Email already registered"
        )
    else:
        new_gestor = GestorRepository.createGestor(Gestor(**new_gestor.model_dump()), database)
        return new_gestor

@router.put("/{id_gestor}")
async def updateGestorById(id_gestor: int, gestor_data: GestorBase, database: Session = Depends(getDatabase)):
    gestor = GestorRepository.getGestorById(id_gestor, database)
    if gestor:
        updated_gestor = GestorRepository.updateGestor(Gestor(id_usuario = id_gestor, **gestor_data.model_dump()), database)
        return updated_gestor

@router.delete("/{id_gestor}")
async def deleteGestor(id_gestor: int, database: Session = Depends(getDatabase)):
    gestor = GestorRepository.getGestorById(id_gestor, database)
    if not gestor:
        raise HTTPException(
                status_code=404, 
                detail="Gestor não encontrado"
            )
    success = GestorRepository.deleteGestor(gestor, database)
    if not success:
        raise HTTPException(
            status_code=500, 
            detail="Erro ao deletar candidato"
        )
    return Response(status_code = status.HTTP_204_NO_CONTENT)
    