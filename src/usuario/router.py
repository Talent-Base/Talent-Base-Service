from fastapi import APIRouter, HTTPException, Depends, Response, status
from sqlalchemy.orm import Session

from ..database import engine, Base, getDatabase
from ..security import getPasswordHash
from .repository import UsuarioRepository
from .schema import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from ..models import Usuario, Candidato, Gestor

from ..candidato.repository import CandidatoRepository
from ..gestor.repository import GestorRepository

from ..auth.repository import getCurrentActiveUser

Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def getUsuarios(database: Session = Depends(getDatabase)):
    usuarios = UsuarioRepository.getAllUsuarios(database)
    return usuarios


@router.get("/{id_usuario}")
async def getUsuarioById(id_usuario: str, database: Session = Depends(getDatabase)):
    usuario = UsuarioRepository.getUsuarioById(id_usuario, database)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario


@router.post("/", response_model=UsuarioResponse)
async def createUsuario(
    usuario_data: UsuarioCreate, database: Session = Depends(getDatabase)
):
    usuario_already_exists = UsuarioRepository.usuarioExistsByEmail(
        usuario_data.email, database
    )
    if usuario_already_exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        usuario_data.senha = getPasswordHash(usuario_data.senha)
        new_usuario = UsuarioRepository.createUsuario(
            Usuario(**usuario_data.model_dump()), database
        )
        if new_usuario.papel == "candidato":
            CandidatoRepository.createCandidato(
                Candidato(
                    id_candidato=new_usuario.id,
                    nome=usuario_data.nome,
                    email=usuario_data.email,
                ),
                database,
            )
        elif new_usuario.papel == "gestor":
            GestorRepository.createGestor(
                Gestor(
                    id_gestor=new_usuario.id,
                    nome=usuario_data.nome,
                    email=usuario_data.email,
                ),
                database,
            )
        return new_usuario


@router.put("/{id_usuario}")
async def updateUsuarioById(
    id_usuario: int,
    usuario_data: UsuarioUpdate,
    database: Session = Depends(getDatabase),
    current_user: Usuario = Depends(getCurrentActiveUser),
):
    if id_usuario != current_user.id:
        raise HTTPException(
            status_code=403, detail="Você não tem permissão para editar este usuário."
        )
    usuario = UsuarioRepository.getUsuarioById(id_usuario, database)
    if usuario:
        updated_usuario = UsuarioRepository.updateUsuario(
            Usuario(id=id_usuario, **usuario_data.model_dump(exclude_unset=True)),
            database,
        )
        return updated_usuario


@router.delete("/{id_usuario}")
async def deleteUsuario(id_usuario: int, database: Session = Depends(getDatabase)):
    usuario = UsuarioRepository.getUsuarioById(id_usuario, database)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    success = UsuarioRepository.deleteUsuario(usuario, database)
    if not success:
        raise HTTPException(status_code=500, detail="Erro ao deletar usuário")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
