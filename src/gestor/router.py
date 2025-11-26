from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session

from src.empresa.repository import EmpresaRepository
from src.empresa.schema import EmpresaBase

from ..database import engine, Base, getDatabase
from .repository import GestorRepository
from .schema import GestorBase
from ..models import Gestor, VagaDeEmprego

from ..vaga_de_emprego.repository import VagaDeEmpregoRepository
from ..vaga_de_emprego.schema import VagaDeEmpregoBase

Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/gestores",
    tags=["gestores"],
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
        raise HTTPException(status_code=404, detail="Gestor não encontrado")
    return gestor


@router.post("/")
async def createGestor(
    new_gestor: GestorBase,
    empresa_data: EmpresaBase,
    database: Session = Depends(getDatabase),
):
    gestor_already_exists = GestorRepository.gestorExistsByEmail(
        new_gestor.email, database
    )
    if gestor_already_exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    empresa_already_exists = EmpresaRepository.empresaAlredyExists(
        empresa_data.cnpj, empresa_data.nome_empresa, database
    )
    if empresa_already_exists:
        raise HTTPException(status_code=400, detail="Empresa already registered")
    else:
        new_gestor = GestorRepository.createGestor(
            Gestor(**new_gestor.model_dump()), database
        )
        return new_gestor


@router.put("/{id_gestor}")
async def updateGestorById(
    id_gestor: int, gestor_data: GestorBase, database: Session = Depends(getDatabase)
):
    gestor = GestorRepository.getGestorById(id_gestor, database)
    if gestor:
        updated_gestor = GestorRepository.updateGestor(
            Gestor(id_usuario=id_gestor, **gestor_data.model_dump()), database
        )
        return updated_gestor


@router.delete("/{id_gestor}")
async def deleteGestor(id_gestor: int, database: Session = Depends(getDatabase)):
    gestor = GestorRepository.getGestorById(id_gestor, database)
    if not gestor:
        raise HTTPException(status_code=404, detail="Gestor não encontrado")
    success = GestorRepository.deleteGestor(gestor, database)
    if not success:
        raise HTTPException(status_code=500, detail="Erro ao deletar candidato")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{id_gestor}/vaga_de_emprego")
async def createVagaDeEmprego(
    id_gestor: int,
    vaga_de_emprego_data: VagaDeEmpregoBase,
    database: Session = Depends(getDatabase),
):
    new_vaga_de_emprego = VagaDeEmpregoRepository.createVagaDeEmprego(
        VagaDeEmprego(**vaga_de_emprego_data.model_dump()), database
    )
    return new_vaga_de_emprego


@router.put("/{id_gestor}/vaga_de_emprego/{id_vaga_de_emprego}")
async def updateVagaDeEmprego(
    id_gestor: int,
    id_vaga_de_emprego: int,
    vaga_de_emprego_data: VagaDeEmpregoBase,
    database: Session = Depends(getDatabase),
):
    vaga_de_emprego = VagaDeEmpregoRepository.getVagaDeEmpregoById(
        id_vaga_de_emprego, database
    )
    if not vaga_de_emprego:
        raise HTTPException(status_code=404, detail="Vaga de emprego não encontrada")
    updated_vaga_de_emprego = VagaDeEmpregoRepository.updateVagaDeEmprego(
        VagaDeEmprego(
            id_vaga_de_emprego=id_vaga_de_emprego, **vaga_de_emprego_data.model_dump()
        )
    )
    return updated_vaga_de_emprego


@router.delete("/{id_gestor}/vaga_de_emprego/{id_vaga_de_emprego}")
async def deleteVagaDeEmprego(
    id_gestor: int, id_vaga_de_emprego: int, database: Session = Depends(getDatabase)
):
    vaga_de_emprego = VagaDeEmpregoRepository.getVagaDeEmpregoById(
        id_vaga_de_emprego, database
    )
    if not vaga_de_emprego:
        raise HTTPException(status_code=404, detail="Vaga de emprego não encontrada")
    success = VagaDeEmpregoRepository.deleteVagaDeEmprego(vaga_de_emprego, database)
    if not success:
        raise HTTPException(status_code=500, detail="Erro ao deletar vaga de emprego")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
