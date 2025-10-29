import os
import sys
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
import pytest
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[2]))

try:
    dotenv_path = Path(__file__).resolve().parents[2] / ".env.testing"
    load_dotenv(dotenv_path)
except IndexError:
    # Captura erro se a estrutura de pastas for diferente do esperado
    print("Aviso: Caminho do arquivo .env.testing pode estar incorreto. Ignorando...")
    pass

from ..main import app
from ..database import getDatabase, Base

DATABASE_URL = os.getenv('DATABASE_URL', "sqlite:///:memory:")

# Se a URL ainda for None (o que é improvável com o fallback, mas seguro verificar)
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL não pôde ser carregada e nenhum fallback foi definido.")


engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_getDatabase():
    database = TestingSessionLocal()
    yield database
    database.close()

app.dependency_overrides[getDatabase] = override_getDatabase

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_createCandidato():
    response = client.post(
        "/candidatos",
        json={
            "nome": "João Silva",
            "email": "joao.silva@example.com",
            "estado": "SP",
            "cidade": "São Paulo",
            "resumo": "Profissional com experiência em desenvolvimento backend usando Python e FastAPI.",
            "situacao_empregaticia": "Desempregado"
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["nome"] == "João Silva"


@pytest.mark.skip
async def testGetCandidatos():
    pass

@pytest.mark.skip
async def testGetCandidatoById():
    pass

@pytest.mark.skip
async def testCreateCandidato():
    pass

@pytest.mark.skip
async def testUpdateCandidatoById():
    pass

@pytest.mark.skip
async def testDeleteCandidatoById():
    pass