import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..main import app
from ..database import getDatabase, Base
from ..auth.repository import requireAdmin, requireCandidato

from ..models import Usuario


SQLALCHEMY_DATABASE_URL_INTEGRATION = 'sqlite:///./test_admin_integration.db'
engine_integration = create_engine(
	SQLALCHEMY_DATABASE_URL_INTEGRATION, connect_args={'check_same_thread': False}
)
TestingSessionLocal_integration = sessionmaker(
	autocommit=False, autoflush=False, bind=engine_integration
)


def override_getDatabase():
	db = TestingSessionLocal_integration()
	try:
		yield db
	finally:
		db.close()


def override_requireCandidato():
	return Usuario(id=1, nome='teste', email='teste@user.com', papel='candidato')


def override_requireAdmin():
	return Usuario(id=2, nome='admin', email='admin@user.com', papel='admin')


app.dependency_overrides[getDatabase] = override_getDatabase
app.dependency_overrides[requireCandidato] = override_requireCandidato
app.dependency_overrides[requireAdmin] = override_requireAdmin


@pytest.fixture(scope='function', autouse=True)
def setup_and_teardown_db():
	Base.metadata.create_all(bind=engine_integration)
	yield
	TestingSessionLocal_integration().close_all()
	Base.metadata.drop_all(bind=engine_integration)


client = TestClient(app)


@pytest.fixture
def createUsuario():
	payload = {
		'nome': 'teste',
		'email': 'teste@user.com',
		'senha': 'teste123',
		'papel': 'candidato',
	}
	response = client.post('/usuarios/candidato', json=payload)
	return response.json()


@pytest.fixture
def createSecondUsuario():
	payload = {
		'nome': 'teste222',
		'email': 'teste222@user.com',
		'senha': 'teste222123',
		'papel': 'candidato',
	}
	response = client.post('/usuarios/candidato', json=payload)
	return response.json()


def test_updateUsuarioById(createUsuario):
	id_candidato = createUsuario['user']['id']
	payload = {
		'id_candidato': id_candidato,
		'nome': 'novo_teste',
		'email': 'teste@user.com',
		'titulo_profissional': 'Designer',
	}
	response = client.put(f'/candidatos/{id_candidato}', json=payload)
	assert response.status_code == 200
	data = response.json()
	assert data['nome'] == payload['nome']
	assert data['titulo_profissional'] == payload['titulo_profissional']


def test_nonAuthorized_updateUsuarioById(createUsuario, createSecondUsuario):
	id_candidato = 2
	payload = {
		'id_candidato': id_candidato,
		'nome': 'novo_teste',
		'email': 'teste@user.com',
		'titulo_profissional': 'Designer',
	}
	response = client.put(f'/candidatos/{id_candidato}', json=payload)
	assert response.status_code == 403


def test_nonExistent_updateUsuarioById():
	id_candidato = 1
	payload = {
		'id_candidato': id_candidato,
		'nome': 'novo_teste',
		'email': 'teste@user.com',
		'titulo_profissional': 'Designer',
	}
	response = client.put(f'/candidatos/{id_candidato}', json=payload)
	assert response.status_code == 404


def test_deleteCandidatoById(createUsuario):
	id_candidato = createUsuario['user']['id']
	response = client.delete(f'/candidatos/{id_candidato}')
	assert response.status_code == 204


def test_nonExistentCandidato_deleteCandidatoById():
	response = client.delete(f'/candidatos/{999}')
	assert response.status_code == 404
