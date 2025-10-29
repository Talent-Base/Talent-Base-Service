import os
import sys
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
import pytest
from fastapi.testclient import TestClient

# Adiciona o diretório raiz do projeto ao sys.path para importações relativas
# Isso é crucial para que `from ..main import app` funcione em um ambiente de teste.
sys.path.append(str(Path(__file__).resolve().parents[2]))

# --- 1. Carregamento de Variáveis de Ambiente ---
# Tenta carregar o arquivo .env.testing. Ajuste parents[N] conforme sua estrutura.
# Se este arquivo estiver em 'projeto_raiz/candidato/tests/candidato/tests.py',
# parents[2] leva ao 'projeto_raiz'.
try:
    dotenv_path = Path(__file__).resolve().parents[2] / ".env.testing"
    load_dotenv(dotenv_path)
except IndexError:
    # Captura erro se a estrutura de pastas for diferente do esperado
    print("Aviso: Caminho do arquivo .env.testing pode estar incorreto. Ignorando...")
    pass

from ..main import app
from ..database import getDatabase, Base # Ajuste o caminho se necessário

# --- 2. Definição da URL do Banco de Dados ---
# Tenta obter a URL do ambiente, mas usa o SQLite in-memory como FALLBACK para testes.
# O SQLite in-memory é a opção mais segura e rápida para testes unitários.
DATABASE_URL = os.getenv('DATABASE_TEST_URL', "sqlite:///:memory:")

# Se a URL ainda for None (o que é improvável com o fallback, mas seguro verificar)
if DATABASE_URL is None:
    raise ValueError("DATABASE_TEST_URL não pôde ser carregada e nenhum fallback foi definido.")

# --- 3. Configuração do Banco de Dados de Teste ---

print(f"Usando DATABASE_URL para teste: {DATABASE_URL}")

engine = create_engine(
    DATABASE_URL,
    # Necessário apenas para SQLite: permite que várias threads acessem a mesma conexão.
    connect_args={
        "check_same_thread": False,
    },
    # StaticPool garante que a conexão in-memory seja persistente para o escopo do teste.
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria as tabelas antes de todos os testes
Base.metadata.create_all(bind=engine)

# --- 4. Dependência (Dependency Override) ---
# Cria um novo banco de dados (session) para cada teste e o fecha após o uso.
def override_get_db():
    """Retorna uma sessão de banco de dados de teste isolada."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Aplica a substituição da dependência na aplicação
app.dependency_overrides[getDatabase] = override_get_db

client = TestClient(app)

# Você pode definir fixtures aqui, se quiser
# Exemplo de fixture para limpar o banco de dados e obter o cliente
@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Configura o banco de dados antes da sessão de teste."""
    # O Base.metadata.create_all(bind=engine) já faz isso
    yield
    # Não precisamos de Base.metadata.drop_all(bind=engine) para in-memory
    # Se estivéssemos usando um arquivo .db, seria necessário limpar.

@pytest.fixture(scope="function")
def test_client():
    """Fixture que retorna o cliente de teste FastAPI."""
    return client
