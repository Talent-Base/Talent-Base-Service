from fastapi import APIRouter, HTTPException, Depends, Response, status
from sqlalchemy.orm import Session

from src.empresa.repository import EmpresaRepository

from ..database import engine, Base, getDatabase
from ..security import getPasswordHash
from .repository import UsuarioRepository
from .schema import (
	AuthResponse,
	UsuarioCreate,
	UsuarioGestorCreate,
	UsuarioUpdate,
	UsuarioResponse,
)
from ..models import Empresa, Usuario, Candidato, Gestor

from ..candidato.repository import CandidatoRepository
from ..gestor.repository import GestorRepository

from ..auth.repository import (
	createAccessToken,
	createRefreshToken,
	getCurrentActiveUser,
	requireAdmin,
)

Base.metadata.create_all(bind=engine)

router = APIRouter(
	prefix='/usuarios',
	tags=['usuarios'],
	responses={404: {'description': 'Not found'}},
)


@router.get('/')
async def getAllUsuarios(database: Session = Depends(getDatabase)):
	usuarios = UsuarioRepository.getAllUsuarios(database)
	return usuarios


@router.get('/{id_usuario}')
async def getUsuarioById(id_usuario: str, database: Session = Depends(getDatabase)):
	usuario = UsuarioRepository.getUsuarioById(id_usuario, database)
	if not usuario:
		raise HTTPException(status_code=404, detail='Usuário não encontrado')
	return usuario


@router.post('/', response_model=AuthResponse)
async def createUsuario(
	usuario_data: UsuarioCreate, database: Session = Depends(getDatabase)
):
	usuario_already_exists = UsuarioRepository.usuarioExistsByEmail(
		usuario_data.email, database
	)
	if usuario_already_exists:
		raise HTTPException(status_code=400, detail='Email já registrado')
	else:
		usuario_data.senha = getPasswordHash(usuario_data.senha)
		new_usuario = UsuarioRepository.createUsuario(
			Usuario(**usuario_data.model_dump()), database
		)
		if new_usuario.papel == 'candidato':
			CandidatoRepository.createCandidato(
				Candidato(
					id_candidato=new_usuario.id,
					nome=usuario_data.nome,
					email=usuario_data.email,
				),
				database,
			)
		elif new_usuario.papel == 'gestor':
			GestorRepository.createGestor(
				Gestor(
					id_gestor=new_usuario.id,
					nome=usuario_data.nome,
					email=usuario_data.email,
				),
				database,
			)
		access_token = createAccessToken({'sub': new_usuario.email})
		refresh_token = createRefreshToken({'sub': new_usuario.email})
		return {
			'access_token': access_token,
			'refresh_token': refresh_token,
			'user': UsuarioResponse.model_validate(new_usuario),
		}


@router.post('/candidato', response_model=AuthResponse)
async def createUsuarioCandidato(
	usuario_data: UsuarioCreate, database: Session = Depends(getDatabase)
):
	usuario_already_exists = UsuarioRepository.usuarioExistsByEmail(
		usuario_data.email, database
	)
	if usuario_already_exists:
		raise HTTPException(status_code=400, detail='Email já registrado')
	else:
		usuario_data.senha = getPasswordHash(usuario_data.senha)
		new_usuario = UsuarioRepository.createUsuario(
			Usuario(**usuario_data.model_dump()), database
		)
		CandidatoRepository.createCandidato(
			Candidato(
				id_candidato=new_usuario.id,
				nome=usuario_data.nome,
				email=usuario_data.email,
			),
			database,
		)

		access_token = createAccessToken({'sub': new_usuario.email})
		refresh_token = createRefreshToken({'sub': new_usuario.email})
		return {
			'access_token': access_token,
			'refresh_token': refresh_token,
			'user': UsuarioResponse.model_validate(new_usuario),
		}


@router.post('/gestor', response_model=AuthResponse)
async def createUsuarioGestor(
	usuario_data: UsuarioGestorCreate, database: Session = Depends(getDatabase)
):
	usuario_already_exists = UsuarioRepository.usuarioExistsByEmail(
		usuario_data.email, database
	)
	empresa_already_exists = EmpresaRepository.empresaAlredyExists(
		usuario_data.empresa.cnpj, usuario_data.empresa.nome_empresa, database
	)
	if usuario_already_exists or empresa_already_exists:
		raise HTTPException(
			status_code=400,
			detail='Email already registered'
			if usuario_already_exists
			else 'Empresa already registered',
		)
	else:
		usuario_data.senha = getPasswordHash(usuario_data.senha)
		new_usuario = UsuarioRepository.createUsuario(
			Usuario(
				nome=usuario_data.nome,
				email=usuario_data.email,
				senha=usuario_data.senha,
				papel=usuario_data.papel,
			),
			database,
		)
		new_empresa = EmpresaRepository.createEmpresa(
			Empresa(**usuario_data.empresa.model_dump()), database
		)
		GestorRepository.createGestor(
			Gestor(
				id_gestor=new_usuario.id,
				nome=usuario_data.nome,
				email=usuario_data.email,
				id_empresa=new_empresa.id_empresa,
			),
			database,
		)
		access_token = createAccessToken({'sub': new_usuario.email})
		refresh_token = createRefreshToken({'sub': new_usuario.email})
		return {
			'access_token': access_token,
			'refresh_token': refresh_token,
			'user': UsuarioResponse.model_validate(new_usuario),
		}


@router.put('/{id_usuario}')
async def updateUsuarioById(
	id_usuario: int,
	usuario_data: UsuarioUpdate,
	database: Session = Depends(getDatabase),
	current_user: Usuario = Depends(getCurrentActiveUser),
):
	if id_usuario != current_user.id:
		raise HTTPException(
			status_code=403, detail='Você não tem permissão para editar este usuário.'
		)
	usuario = UsuarioRepository.getUsuarioById(id_usuario, database)
	if usuario:
		updated_usuario = UsuarioRepository.updateUsuario(
			Usuario(id=id_usuario, **usuario_data.model_dump(exclude_unset=True)),
			database,
		)
		return updated_usuario


@router.delete('/{id_usuario}')
async def deleteUsuarioById(
	id_usuario: int,
	database: Session = Depends(getDatabase),
	current_user: Usuario = Depends(requireAdmin),
):
	usuario = UsuarioRepository.getUsuarioById(id_usuario, database)
	if not usuario:
		raise HTTPException(status_code=404, detail='Usuário não encontrado')
	success = UsuarioRepository.deleteUsuario(usuario, database)
	if not success:
		raise HTTPException(status_code=500, detail='Erro ao deletar usuário')
	return Response(status_code=status.HTTP_204_NO_CONTENT)
