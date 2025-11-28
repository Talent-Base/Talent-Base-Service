import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..main import app
from ..database import getDatabase, Base
from ..auth.repository import requireAdmin, requireGestor

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


def override_requireGestor():
	return Usuario(id=1, nome='teste', email='teste@user.com', papel='gestor')


def override_requireAdmin():
	return Usuario(id=2, nome='admin', email='admin@user.com', papel='admin')


app.dependency_overrides[getDatabase] = override_getDatabase
app.dependency_overrides[requireGestor] = override_requireGestor
app.dependency_overrides[requireAdmin] = override_requireAdmin


@pytest.fixture(scope='function', autouse=True)
def setup_and_teardown_db():
	Base.metadata.create_all(bind=engine_integration)
	yield
	TestingSessionLocal_integration().close_all()
	Base.metadata.drop_all(bind=engine_integration)


client = TestClient(app)


@pytest.fixture
def createGestor():
	payload = {
		'nome': 'teste',
		'email': 'teste@user.com',
		'senha': 'teste123',
		'papel': 'gestor',
		'empresa': {
			'nome_empresa': 'teste_empresa',
			'cnpj': '11.111.111/1111-11',
			'cidade': 'Brasília',
			'estado': 'DF',
		},
	}

	response = client.post('/usuarios/gestor', json=payload)
	return response.json()


@pytest.fixture
def createSecondUsuario():
	payload = {
		'nome': 'teste222',
		'email': 'teste222@user.com',
		'senha': 'teste222123',
		'papel': 'gestor',
		'empresa': {
			'nome_empresa': 'teste_empresa222',
			'cnpj': '11.222.111/2222-11',
			'cidade': 'Brasília',
			'estado': 'DF',
		},
	}

	response = client.post('/usuarios/gestor', json=payload)
	return response.json()


def test_updateGestor(createGestor):
	payload = {
		'nome': 'teste_novo',
		'email': 'teste@user.com',
	}

	response = client.put('/usuarios/gestor', json=payload)
	assert response.status_code == 200
	data = response.json()
	assert data['user']['nome'] == payload['email']
