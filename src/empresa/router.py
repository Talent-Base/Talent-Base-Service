from fastapi import APIRouter, HTTPException, Depends, Response, status
from sqlalchemy.orm import Session

from ..database import engine, Base, getDatabase
from .repository import EmpresaRepository
from .schema import EmpresaBase
from ..models import Empresa

from ..vaga_de_emprego.repository import VagaDeEmpregoRepository
from ..gestor.repository import GestorRepository

Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/empresas",
    tags=["empresas"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def getEmpresas(database: Session = Depends(getDatabase)):
    empresas = EmpresaRepository.getAllEmpresas(database)
    return empresas


@router.get("/")
async def getEmpresaById(id_empresa: int, database: Session = Depends(getDatabase)):
    empresa = EmpresaRepository.getEmpresaById(id_empresa, database)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return empresa


@router.post("/")
async def createEmpresa(
    empresa_data: EmpresaBase, database: Session = Depends(getDatabase)
):
    empresa_already_exists = EmpresaRepository.empresaExistsByCnpj(
        empresa_data.cnpj, database
    )
    if empresa_already_exists:
        raise HTTPException(status_code=400, detail="Empresa already registered")
    else:
        new_empresa = EmpresaRepository.createEmpresa(
            Empresa(**empresa_data.model_dump()), database
        )
        return new_empresa


@router.delete("/{id_empresa}")
async def deleteEmpresaById(id_empresa: int, database: Session = Depends(getDatabase)):
    empresa = EmpresaRepository.getEmpresaById(id_empresa, database)
    if empresa:
        deleted_experiencia = EmpresaRepository.deleteEmpresa(empresa, database)
        return deleted_experiencia


@router.put("/{id_empresa}")
async def updateEmpresaById(
    id_empresa: int, empresa_data: EmpresaBase, database: Session = Depends(getDatabase)
):
    empresa = EmpresaRepository.getEmpresaById(id_empresa, database)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    success = EmpresaRepository.deleteEmpresa(empresa, database)
    if not success:
        raise HTTPException(status_code=500, detail="Erro ao deletar candidato")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{id_empresa}/vagas_de_emprego")
async def getEmpresasVagaDeEmprego(
    id_empresa: int, database: Session = Depends(getDatabase)
):
    vagas_de_emprego = VagaDeEmpregoRepository.getVagaDeEmpregoByEmpresaId(
        id_empresa, database
    )
    if not vagas_de_emprego:
        raise HTTPException(status_code=404, detail="Vagas de emprego não encontradas")
    return vagas_de_emprego


@router.get("{id_empresa}/getores")
async def getEmpresasGestores(
    id_empresa: int, database: Session = Depends(getDatabase)
):
    gestores = GestorRepository.getGestoresByEmpresaId(id_empresa, database)
    if not gestores:
        raise HTTPException(status_code=404, detail="Gestores não encontradas")
    return gestores
