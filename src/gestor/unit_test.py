import sys
from pathlib import Path
import pytest


sys.path.append(str(Path(__file__).resolve().parents[1]))

from ..models import Gestor, Empresa, Usuario
from .repository import GestorRepository
from ..empresa.repository import EmpresaRepository
from ..usuario.repository import UsuarioRepository


def make_usuario_e_gestor(nome, email, id_empresa=None):
	usuario = Usuario(
		nome=nome,
		email=email,
		senha='hash',
		papel='gestor',
		ativo=True,
	)

	gestor = Gestor(nome=nome, email=email, id_empresa=id_empresa)

	usuario.gestor = gestor
	return usuario, gestor


def make_gestores(valid_empresa_id: bool = True):
	if valid_empresa_id:
		id_empresa = 1
	else:
		id_empresa = -1

	dados = [
		('Mariana Villasboas', 'villasboas.mariana@empresaa.br', id_empresa),
		('Valquíria Saes', 'saes.val@empresaa.br', id_empresa),
		('Carlos Gomide', 'gom.carlos@empresaa.br', None),
	]

	gestores = []
	for nome, email, emp_id in dados:
		gestores.append(make_usuario_e_gestor(nome, email, emp_id))

	return gestores


@pytest.fixture
def add_empresa(db):
	empresa = Empresa(
		id_empresa=1,
		nome_empresa='Empresa A',
		cnpj='0000000000000',
		cidade='Cidade A',
		estado='AA',
		descricao='A Empresa A é a responsavel pela saúde',
	)
	return EmpresaRepository.createEmpresa(empresa, db)


@pytest.fixture
def sample_gestor(add_empresa):
	usuario, gestor = make_usuario_e_gestor(
		nome='Mariana Villasboas',
		email='villasboas.mariana@empresaa.br',
		id_empresa=add_empresa.id_empresa,
	)
	return usuario, gestor


@pytest.mark.parametrize('usuario_gestor', make_gestores())
def test_createGestor(usuario_gestor, add_empresa, db):
	usuario, gestor = usuario_gestor

	UsuarioRepository.createUsuario(usuario, db)

	result = GestorRepository.createGestor(gestor, db)

	assert result.id_gestor == usuario.id
	assert result.nome == gestor.nome
	assert db.query(Gestor).count() == 1


@pytest.mark.parametrize('usuario_gestor', make_gestores())
def test_gestorExistsByEmail(usuario_gestor, add_empresa, db):
	usuario, gestor = usuario_gestor

	UsuarioRepository.createUsuario(usuario, db)
	GestorRepository.createGestor(gestor, db)

	result = GestorRepository.gestorExistsByEmail(gestor.email, db)

	assert result is True
	assert db.query(Gestor).count() == 1


@pytest.mark.parametrize('usuario_gestor', make_gestores())
def test_nonExistentGestor_gestorExistsByEmail(usuario_gestor, db):
	_, gestor = usuario_gestor

	result = GestorRepository.gestorExistsByEmail(gestor.email, db)

	assert result is False
	assert db.query(Gestor).count() == 0


@pytest.mark.parametrize('usuario_gestor', make_gestores())
def test_getGestorById(usuario_gestor, add_empresa, db):
	usuario, gestor = usuario_gestor

	UsuarioRepository.createUsuario(usuario, db)

	created = GestorRepository.createGestor(gestor, db)

	result = GestorRepository.getGestorById(created.id_gestor, db)

	assert result.id_gestor == created.id_gestor
	assert result.nome == created.nome


def test_nonExistentGestor_getGestorById(db):
	result = GestorRepository.getGestorById(-1, db)
	assert result is None


@pytest.mark.parametrize(
	'novo_email', ['novo1@example.com', 'novo2@example.com', 'novo3@example.com']
)
def test_updateGestor(sample_gestor, novo_email, db):
	usuario, gestor = sample_gestor

	GestorRepository.createGestor(gestor, db)

	GestorRepository.createGestor(gestor, db)

	gestor.email = novo_email
	result = GestorRepository.updateGestor(gestor, db)

	assert result.email == novo_email


@pytest.mark.parametrize('usuario_gestor', make_gestores())
def test_deleteGestor(usuario_gestor, add_empresa, db):
	usuario, gestor = usuario_gestor

	GestorRepository.createGestor(gestor, db)

	created = GestorRepository.createGestor(gestor, db)

	result = GestorRepository.deleteGestor(created, db)

	assert result is True
	assert db.query(Gestor).count() == 0


@pytest.mark.parametrize('usuario_gestor', make_gestores())
def test_nonExistentGestor_deleteGestor(usuario_gestor, db):
	_, gestor = usuario_gestor

	with pytest.raises(Exception):
		GestorRepository.deleteGestor(gestor, db)