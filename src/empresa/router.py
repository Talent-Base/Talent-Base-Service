from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ..database import engine, Base, getDatabase
from .repository import EmpresaRepository
from .schema import EmpresaBase
from ..models import Empresa

Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix = "/empresas",
    tags = ["empresas"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def getEmpresas(database: Session = Depends(getDatabase)):
    empresas = EmpresaRepository.getAllEmpresas(database)
    return empresas

@router.get("/")
async def getEmpresaById(id_empresa: int, database: Session = Depends(getDatabase)):
    empresa = EmpresaRepository.getEmpresaById(id_empresa, database)
    return empresa

@router.post("/")
async def createEmpresa(empresa_data: EmpresaBase, database: Session = Depends(getDatabase)):
    empresa_already_exists = EmpresaRepository.empresaExistsByName(empresa_data.nome, database)
    if empresa_already_exists:
        raise HTTPException(
                status_code=400,
                detail="Empresa already registered"
        )
    else:
        new_empresa = EmpresaRepository.createEmpresa(empresa_data, database)
        return new_empresa

@router.delete("/{id_empresa}")
async def deleteEmpresaById(id_empresa: int, database: Session = Depends(getDatabase)):
    empresa = EmpresaRepository.getEmpresaById(id_empresa, database)
    if empresa:
        deleted_experiencia = EmpresaRepository.deleteEmpresa(empresa, database)
        return deleted_experiencia

@router.put("/{id_empresa}")
async def updateEmpresaById(id_empresa: int, empresa_data: EmpresaBase, database: Session = Depends(getDatabase)):
    empresa = EmpresaRepository.getEmpresaById(id_empresa, database)
    if empresa:
        updated_empresa = EmpresaRepository.updateEmpresa(Empresa(id_empresa = id_empresa, **empresa_data.model_dump()), database)
        return updated_empresa