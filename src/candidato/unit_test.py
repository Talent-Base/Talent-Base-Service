import sys
from pathlib import Path
import pytest


sys.path.append(str(Path(__file__).resolve().parents[1]))

from ..models import Candidato, Usuario
from .repository import CandidatoRepository
from ..usuario.repository import UsuarioRepository

# # E não é q testes funcionam?

@pytest.fixture
def make_usuarios(db):
	usuarios = [
		Usuario(
			nome='João Silva',
			email='joao@example.com',
			senha='joaosilva',
			papel='candidato',
		),
		Usuario(
			nome='Maria Souza',
			email='maria@example.com',
			senha='mariasouza',
			papel='candidato',
		),
		Usuario(
			nome='Carlos Lima',
			email='carlos@example.com',
			senha='carloslima',
			papel='candidato',
		),
	]
	persisted_usuarios = []
	for usuario in usuarios:
		UsuarioRepository.createUsuario(usuario, db)
		persisted_usuarios.append(usuario)
	return persisted_usuarios


def make_candidatos():
	return [
		Candidato(
			id_candidato=1,
			nome='João Silva',
			email='joao@example.com',
			estado='SP',
			cidade='São Paulo',
			resumo='Experiência em FastAPI',
			situacao_empregaticia='Desempregado',
		),
		Candidato(
			id_candidato=2,
			nome='Maria Souza',
			email='maria@example.com',
			estado='RJ',
			cidade='Rio de Janeiro',
			resumo='Desenvolvedora backend',
		),
		Candidato(
			id_candidato=3,
			nome='Carlos Lima',
			email='carlos@example.com',
		),
	]


@pytest.fixture
def sample_candidato(db):
	usuario = Usuario(
		nome='João Silva', email='joao@example.com', senha='123123', papel='candidato'
	)
	result = UsuarioRepository.createUsuario(usuario, db)
	return result


@pytest.mark.parametrize(
	'index, nome, email, estado, cidade, resumo, situacao_empregaticia',
	[
		(
			0,
			'João Silva',
			'joao@example.com',
			'SP',
			'São Paulo',
			'Experiência em FastAPI',
			'Desempregado',
		),
		(
			1,
			'Maria Souza',
			'maria@example.com',
			'RJ',
			'Rio de Janeiro',
			'Desenvolvedora backend',
			None,
		),
		(2, 'Carlos Lima', 'carlos@example.com', None, None, None, None),
	],
)
def test_createCandidato(
	index, nome, email, estado, cidade, resumo, situacao_empregaticia, db, make_usuarios
):
	usuario = make_usuarios[index]
	usuario_id = usuario.id

	candidato_data = Candidato(
		id_candidato=usuario_id,
		nome=nome,
		email=email,
		estado=estado,
		cidade=cidade,
		resumo=resumo,
		situacao_empregaticia=situacao_empregaticia,
	)

	result = CandidatoRepository.createCandidato(candidato_data, db)

	assert result.id_candidato == usuario_id
	assert result.nome == nome
	assert db.query(Candidato).count() == 1


@pytest.mark.parametrize(
	'index, nome, email, estado, cidade, resumo, situacao_empregaticia',
	[
		(
			0,
			'João Silva',
			'joao@example.com',
			'SP',
			'São Paulo',
			'Experiência em FastAPI',
			'Desempregado',
		),
		(
			1,
			'Maria Souza',
			'maria@example.com',
			'RJ',
			'Rio de Janeiro',
			'Desenvolvedora backend',
			None,
		),
		(2, 'Carlos Lima', 'carlos@example.com', None, None, None, None),
	],
)
def test_candidatoExistsByEmail(
	index, nome, email, estado, cidade, resumo, situacao_empregaticia, db, make_usuarios
):
	usuario = make_usuarios[index]
	usuario_id = usuario.id

	candidato_data = Candidato(
		id_candidato=usuario_id,
		nome=nome,
		email=email,
		estado=estado,
		cidade=cidade,
		resumo=resumo,
		situacao_empregaticia=situacao_empregaticia,
	)

	CandidatoRepository.createCandidato(candidato_data, db)
	result = CandidatoRepository.candidatoExistsByEmail(candidato_data.email, db)

	assert result is True
	assert db.query(Candidato).count() == 1


@pytest.mark.parametrize(
	'email',
	[
		'joao@example.com',
		'maria@example.com',
		'carlos@example.com',
	],
)
def test_nonExistentCandidato_candidatoExistsByEmail(email, db):
	result = CandidatoRepository.candidatoExistsByEmail(email, db)

	assert result is False
	assert db.query(Candidato).count() == 0


@pytest.mark.parametrize(
	'index, nome, email, estado, cidade, resumo, situacao_empregaticia',
	[
		(
			0,
			'João Silva',
			'joao@example.com',
			'SP',
			'São Paulo',
			'Experiência em FastAPI',
			'Desempregado',
		),
		(
			1,
			'Maria Souza',
			'maria@example.com',
			'RJ',
			'Rio de Janeiro',
			'Desenvolvedora backend',
			None,
		),
		(2, 'Carlos Lima', 'carlos@example.com', None, None, None, None),
	],
)
def test_getCandidatoById(
	index, nome, email, estado, cidade, resumo, situacao_empregaticia, db, make_usuarios
):
	usuario = make_usuarios[index]
	usuario_id = usuario.id

	candidato_data = Candidato(
		id_candidato=usuario_id,
		nome=nome,
		email=email,
		estado=estado,
		cidade=cidade,
		resumo=resumo,
		situacao_empregaticia=situacao_empregaticia,
	)

	CandidatoRepository.createCandidato(candidato_data, db)

	result = CandidatoRepository.getCandidatoById(candidato_data.id_candidato, db)

	assert result.nome == candidato_data.nome


@pytest.mark.parametrize(
	'novo_email', ['novo1@example.com', 'novo2@example.com', 'novo3@example.com']
)
def test_updateCandidato(novo_email, sample_candidato, db):
	candidato_data = Candidato(
		id_candidato=1,
		nome=sample_candidato.nome,
		email=sample_candidato.email,
	)

	candidato = CandidatoRepository.createCandidato(candidato_data, db)
	candidato.email = novo_email

	result = CandidatoRepository.updateCandidato(candidato, db)

	assert result.email == novo_email
	assert result.nome == candidato.nome


@pytest.mark.parametrize(
	'index, nome, email, estado, cidade, resumo, situacao_empregaticia',
	[
		(
			0,
			'João Silva',
			'joao@example.com',
			'SP',
			'São Paulo',
			'Experiência em FastAPI',
			'Desempregado',
		),
		(
			1,
			'Maria Souza',
			'maria@example.com',
			'RJ',
			'Rio de Janeiro',
			'Desenvolvedora backend',
			None,
		),
		(2, 'Carlos Lima', 'carlos@example.com', None, None, None, None),
	],
)
def test_deleteCandidato(
	index, nome, email, estado, cidade, resumo, situacao_empregaticia, db, make_usuarios
):
	usuario = make_usuarios[index]
	usuario_id = usuario.id

	candidato_data = Candidato(
		id_candidato=usuario_id,
		nome=nome,
		email=email,
		estado=estado,
		cidade=cidade,
		resumo=resumo,
		situacao_empregaticia=situacao_empregaticia,
	)

	CandidatoRepository.createCandidato(candidato_data, db)
	result = CandidatoRepository.deleteCandidato(candidato_data, db)

	assert result is True
	assert db.query(Candidato).count() == 0


@pytest.mark.parametrize('id', [11, 22, 33])
def test_nonExistentCandidato_deleteCandidato(id, db):
	with pytest.raises(Exception):
		CandidatoRepository.deleteCandidato(id, db)
