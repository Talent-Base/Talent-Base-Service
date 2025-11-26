from typing import List
from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session

from ..models import Usuario
from ..usuario.repository import UsuarioRepository

from .schema import StatsBase, ToggleStatusRequest

from .repository import AdminRepository

from ..auth.repository import requireAdmin

from ..database import engine, Base, getDatabase


Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/admin",
    tags=["candidatos"],
    responses={404: {"description": "Not found"}},
)


@router.get("/stats", response_model=StatsBase)
async def getAdminStatistics(
    database: Session = Depends(getDatabase),
    current_user: Usuario = Depends(requireAdmin),
):
    statistics = AdminRepository.getStatistics(database)
    return statistics


@router.put("/toggle_user_status/{id_usuario}")
async def toggleUserStatus(
    id_usuario: int,
    payload: ToggleStatusRequest,
    database: Session = Depends(getDatabase),
    current_user: Usuario = Depends(requireAdmin),
):
    usuario = UsuarioRepository.getUsuarioById(id_usuario, database)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    success = AdminRepository.toggleUserStatus(payload.new_status, usuario, database)
    if not success:
        raise HTTPException(
            status_code=400, detail="Não foi possível alterar o status do usuário"
        )
    return {"status": "ok", "new_status": payload.new_status}
