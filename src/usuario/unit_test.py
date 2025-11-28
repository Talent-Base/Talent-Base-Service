import sys
from pathlib import Path
import pytest


sys.path.append(str(Path(__file__).resolve().parents[1]))

from ..models import Usuario
from .repository import UsuarioRepository


def make_usuarios():
	return [
		Usuario(nome='Joao', email='joao.email.com', senha='teste', papel='candidato'),
		Usuario(nome='Maria', email='maria.email.com', senha='teste', papel='gestor'),
		Usuario(nome='adm', email='adm.email.com', senha='teste', papel='admin'),
	]


@pytest.fixture
def sample_usuario():
	return Usuario(
		nome='Joao', email='joao.email.com', senha='teste', papel='candidato'
	)


@pytest.mark.parametrize('usuario', make_usuarios())
def test_createUsuario(usuario, db):
	result = UsuarioRepository.createUsuario(usuario, db)

	assert result.id is not None
	assert result.nome == usuario.nome
	assert db.query(Usuario).count() == 1


@pytest.mark.parametrize('usuario', make_usuarios())
def test_usuarioExistsByEmail(usuario, db):
	UsuarioRepository.createUsuario(usuario, db)
	result = UsuarioRepository.usuarioExistsByEmail(usuario.email, db)

	assert result
	assert db.query(Usuario).count() == 1


@pytest.mark.parametrize('usuario', make_usuarios())
def test_nonExistentUsuario_usuarioExistsByEmail(usuario, db):
	result = UsuarioRepository.usuarioExistsByEmail(usuario.email, db)

	assert not result
	assert db.query(Usuario).count() == 0


@pytest.mark.parametrize('usuario', make_usuarios())
def test_getUsuarioById(usuario, db):
	created_usuario = UsuarioRepository.createUsuario(usuario, db)
	id_created_user = created_usuario.id
	result = UsuarioRepository.getUsuarioById(id_created_user, db)

	assert result.nome == usuario.nome


def test_nonExistentUsuario_getUsuarioById(db):
	result = UsuarioRepository.getUsuarioById(1, db)

	assert result is None


@pytest.mark.parametrize(
	'novo_email', ['novo1@example.com', 'novo2@example.com', 'novo3@example.com']
)
def test_updateUsuario(sample_usuario, novo_email, db):
	UsuarioRepository.createUsuario(sample_usuario, db)
	sample_usuario.email = novo_email
	result = UsuarioRepository.updateUsuario(sample_usuario, db)

	assert result.nome == sample_usuario.nome
	assert result.email == novo_email


@pytest.mark.parametrize('usuario', make_usuarios())
def test_deleteUsuario(usuario, db):
	UsuarioRepository.createUsuario(usuario, db)
	result = UsuarioRepository.deleteUsuario(usuario, db)

	assert result
	assert db.query(Usuario).count() == 0


@pytest.mark.parametrize('usuario', make_usuarios())
def test_nonExistentUsuario_deleteUsuario(usuario, db):
	with pytest.raises(Exception):
		UsuarioRepository.deleteUsuario(usuario, db)
