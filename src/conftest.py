import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import pytest

from sqlalchemy import create_engine, event, Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

try:
	dotenv_path = project_root / '.env.testing'
	if dotenv_path.exists():
		load_dotenv(dotenv_path)
		print(f'Carregado .env.testing de: {dotenv_path}')
	else:
		print('Aviso: .env.testing não encontrado. Usando variáveis de ambiente.')
except Exception as e:
	print(f'Erro ao carregar .env.testing: {e}')
	pass

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///:memory:')

print(f'--- INICIANDO TESTES COM DATABASE: {DATABASE_URL} ---')

engine_args = {}

if DATABASE_URL.startswith('sqlite'):
	print('--- Configurando para SQLite (local) ---')
	engine_args['connect_args'] = {'check_same_thread': False}
	engine_args['poolclass'] = StaticPool
else:
	print('--- Configurando para PostgreSQL (Docker) ---')
	pass

engine = create_engine(DATABASE_URL, **engine_args)

if DATABASE_URL.startswith('sqlite'):

	@event.listens_for(Engine, 'connect')
	def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
		"""Ativa o suporte a Foreign Keys no SQLite."""
		print('--- Habilitando Foreign Keys (PRAGMA) para SQLite ---')
		cursor = dbapi_connection.cursor()
		cursor.execute('PRAGMA foreign_keys=ON')
		cursor.close()


try:
	from src.database import Base
except ImportError:
	from .database import Base


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope='session')
def db_engine():
	"""
	Fixture de escopo de sessão para criar e derrubar
	as tabelas do banco de dados uma vez por execução de teste.
	"""
	print('Criando tabelas...')
	Base.metadata.create_all(bind=engine)
	yield engine
	print('\nDerrubando tabelas...')
	Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='function')
def db(db_engine):
	"""
	Fixture principal que os testes usarão.
	Fornece uma sessão de banco de dados isolada para cada teste.
	"""
	connection = db_engine.connect()
	transaction = connection.begin()
	session = TestingSessionLocal(bind=connection)
	yield session
	session.close()
	transaction.rollback()
	connection.close()
