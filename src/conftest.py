import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import pytest

from sqlalchemy import create_engine, event, Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# --- Carregamento de Configuração ---
# Adiciona a raiz do projeto ao sys.path para encontrar os módulos
# (Assumindo que conftest.py está em 'src/tests/')
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

try:
    # Carrega o .env.testing (se existir) para testes locais
    dotenv_path = project_root / ".env.testing"
    if dotenv_path.exists():
        load_dotenv(dotenv_path)
        print(f"Carregado .env.testing de: {dotenv_path}")
    else:
        print("Aviso: .env.testing não encontrado. Usando variáveis de ambiente.")
except Exception as e:
    print(f"Erro ao carregar .env.testing: {e}")
    pass

# --- A LÓGICA CONDICIONAL ---

# Pega a DATABASE_URL do ambiente (seja do Docker ou do .env.testing)
# Fallback para SQLite em memória se NADA for definido
DATABASE_URL = os.getenv('DATABASE_URL', "sqlite:///:memory:")

print(f"--- INICIANDO TESTES COM DATABASE: {DATABASE_URL} ---")

# Argumentos padrão para o create_engine
engine_args = {}

# VERIFICAÇÃO: Aplica configurações específicas do SQLite
if DATABASE_URL.startswith("sqlite"):
    print("--- Configurando para SQLite (local) ---")
    engine_args["connect_args"] = {"check_same_thread": False}
    # StaticPool é bom para testes em memória/arquivo
    engine_args["poolclass"] = StaticPool
else:
    # Para PostgreSQL, não passa argumentos extras
    print("--- Configurando para PostgreSQL (Docker) ---")
    # Usa o pool de conexão padrão do SQLAlchemy (QueuePool)
    pass

# Cria o engine com os argumentos corretos
engine = create_engine(DATABASE_URL, **engine_args)

# O listener do PRAGMA TAMBÉM deve ser condicional
if DATABASE_URL.startswith("sqlite"):
    @event.listens_for(Engine, "connect")
    def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
        """Ativa o suporte a Foreign Keys no SQLite."""
        print("--- Habilitando Foreign Keys (PRAGMA) para SQLite ---")
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

# --- Fixtures do Pytest ---

# Importa o Base declarativo da sua aplicação
# Ajuste o caminho 'from ..database import Base' se o seu arquivo database.py
# estiver em um local diferente (ex: src/database.py)
try:
    from src.database import Base 
except ImportError:
    # Tenta um caminho relativo se o primeiro falhar
    from .database import Base

# Cria a sessão de teste
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    """
    Fixture de escopo de sessão para criar e derrubar
    as tabelas do banco de dados uma vez por execução de teste.
    """
    print("Criando tabelas...")
    Base.metadata.create_all(bind=engine)
    yield engine
    print("\nDerrubando tabelas...")
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db(db_engine):
    """
    Fixture principal que os testes usarão.
    Fornece uma sessão de banco de dados isolada (transaction) para cada teste.
    """
    connection = db_engine.connect()
    # Inicia uma transação "externa"
    transaction = connection.begin()
    # Vincula a sessão a essa conexão
    session = TestingSessionLocal(bind=connection)

    yield session

    # Limpeza: desfaz tudo após o teste
    session.close()
    # Reverte a transação, limpando quaisquer dados do teste
    transaction.rollback()
    connection.close()
