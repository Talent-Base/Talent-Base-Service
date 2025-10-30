from fastapi import APIRouter, HTTPException, Depends, Response, status
from sqlalchemy.orm import Session

from ..database import engine, Base, getDatabase
from .repository import VagaDeEmpregoRepository
from .schema import VagaDeEmpregoBase
from ..models import VagaDeEmprego

from ..candidatura.repository import CandidaturaRepository

Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix = "/vagas_de_emprego",
    tags = ["vagas de emprego"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def getVagasDeEmprego(database: Session = Depends(getDatabase)):
    vagas_de_emprego = VagaDeEmpregoRepository.getAllVagasDeEmprego(database)
    return vagas_de_emprego

@router.get("/")
async def getVagaDeEmpregoById(id_vaga_de_emprego: int, database: Session = Depends(getDatabase)):
    vagas_de_emprego = VagaDeEmpregoRepository.getVagaDeEmpregoById(id_vaga_de_emprego, database)
    return vagas_de_emprego

@router.post("/")
async def createVagaDeEmprego(vaga_de_emprego_data: VagaDeEmpregoBase, database: Session = Depends(getDatabase)):
    new_vaga_de_emprego = VagaDeEmpregoRepository.createVagaDeEmprego(VagaDeEmprego(**vaga_de_emprego_data.model_dump()), database)
    return new_vaga_de_emprego

@router.delete("/{id_vaga_de_emprego}")
async def deleteVagaDeEmpregoById(id_vaga_de_emprego: int, database: Session = Depends(getDatabase)):
    vaga_de_emprego = VagaDeEmpregoRepository.getVagaDeEmpregoById(id_vaga_de_emprego, database)
    if not vaga_de_emprego:
        raise HTTPException(status_code=404, detail="Vaga de emprego não encontrado")
    success = VagaDeEmpregoRepository.deleteVagaDeEmprego(vaga_de_emprego, database)
    if not success:
        raise HTTPException(status_code=500, detail="Erro ao deletar vaga de emprego")
    return Response(status_code = status.HTTP_204_NO_CONTENT)

    
@router.put("/{id_vaga_de_emprego}")
async def updateVagaDeEmpregoById(id_vaga_de_emprego: int, vaga_de_emprego_data: VagaDeEmpregoBase, database: Session = Depends(getDatabase)):
    vaga_de_emprego = VagaDeEmpregoRepository.getVagaDeEmpregoById(id_vaga_de_emprego, database)
    if vaga_de_emprego:
        updated_vaga_de_emprego = VagaDeEmpregoRepository.updateVagaDeEmprego(VagaDeEmprego(id_vaga_de_emprego = id_vaga_de_emprego, **vaga_de_emprego_data.model_dump()), database)
        return updated_vaga_de_emprego
    

@router.get("/{id_vaga_de_emprego}/candidaturas")
async def getVagaDeEmpregosCandidaturas(id_vaga_de_emprego: int, database: Session = Depends(getDatabase)):
    candidaturas = CandidaturaRepository.getCandidaturasByVagaDeEmpregoId(id_vaga_de_emprego, database)
    return candidaturas