import os
from sqlite3 import IntegrityError
import sys
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine, StaticPool, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
import pytest


sys.path.append(str(Path(__file__).resolve().parents[2]))

try:
    dotenv_path = Path(__file__).resolve().parents[2] / ".env.testing"
    load_dotenv(dotenv_path)
except IndexError:
    print("Aviso: Caminho do arquivo .env.testing pode estar incorreto. Ignorando...")
    pass

from ..database import Base
from ..models import Experiencia, Candidato
from .repository import ExperienciaRepository
from ..candidato.repository import CandidatoRepository

DATABASE_URL = os.getenv('DATABASE_URL', "sqlite:///:memory:")

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


@event.listens_for(Engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def add_candidato(db):
    sample = Candidato(
        id_usuario=1,
        nome="João Silva",
        email="joao@example.com",
        estado="SP",
        cidade="São Paulo",
        resumo="Experiência em FastAPI",
        situacao_empregaticia="Desempregado",
    )
    return CandidatoRepository.createCandidato(sample, db)

@pytest.fixture
def sample_experiencia(add_candidato):

    return  Experiencia(
        id_usuario=add_candidato.id_usuario,
        nome_instituicao="TechCorp",
        cargo="Desenvolvedor Backend",
        periodo_experiencia=24,
        descricao="Desenvolvimento de APIs com FastAPI e PostgreSQL",
        nome_curso=None,
        grau_obtido=None,
    )

def make_experiencias(valid: bool = True):

    if valid:
        id=1
    else:
        id=-1
    return [
        Experiencia(
            id_usuario=id,  # João Silva
            nome_instituicao="Empresa X",
            cargo="Desenvolvedor Backend",
            periodo_experiencia=3, 
            descricao="Desenvolvimento de APIs RESTful com FastAPI e Python.",
        ),
        Experiencia(
            id_usuario=id,  
            nome_instituicao="Empresa Y",
            cargo="Desenvolvedora Backend",
            periodo_experiencia=2,  
            #descricao="Responsável pela implementação de microserviços e integração contínua.",
            #nome_curso="Especialização em Arquitetura de Sistemas",
            #grau_obtido="Mestrado",
        ),
        Experiencia(
            id_usuario=id,  
            nome_instituicao="Faculdade Z",
            cargo="Estudante",
            periodo_experiencia=4,  
            descricao="Análise de grandes volumes de dados e criação de relatórios gerenciais.",
            nome_curso="Engenharia de Dados",
            grau_obtido="Graduação",
        ),
    ]

@pytest.mark.parametrize("experiencia", make_experiencias())
def test_createExperiencia(add_candidato, experiencia, db):

    result = ExperienciaRepository.createExperiencia(experiencia, db)

    assert result.id_experiencia is not None
    assert result.nome_instituicao == experiencia.nome_instituicao
    assert result.cargo == experiencia.cargo
    assert result.id_usuario == add_candidato.id_usuario

    experiencias_db = db.query(Experiencia).filter_by(id_usuario=add_candidato.id_usuario).all()
    assert len(experiencias_db) == 1
    assert experiencias_db[0].nome_instituicao == experiencia.nome_instituicao

""" @pytest.mark.parametrize("experiencia", make_experiencias(False))
def test_nonExistentCandidato_createExperiencia(experiencia, db):

    with pytest.raises(IntegrityError):
        ExperienciaRepository.createExperiencia(experiencia, db)
    db.rollback() """


@pytest.mark.parametrize("experiencia", make_experiencias())
def test_getExperienciaByCandidatoId(add_candidato, experiencia, db):
    ExperienciaRepository.createExperiencia(experiencia, db)
    result = ExperienciaRepository.getExperienciasByCandidatoId(add_candidato.id_usuario, db)
    assert len(result) == 1
    assert result[0].id_usuario == add_candidato.id_usuario
    assert result[0].nome_instituicao == experiencia.nome_instituicao


def test_nonExistentCandidato_getExperienciaByCandidatoId(db):
    result = ExperienciaRepository.getExperienciasByCandidatoId(-1, db)
    assert len(result) == 0



@pytest.mark.parametrize(
    "nova_instituicao", 
    ["Instituição 1", "Instituição 2", "Instituição 3"]
)
def test_updateExperienciaById(add_candidato, nova_instituicao, sample_experiencia, db):
    ExperienciaRepository.createExperiencia(sample_experiencia, db)
    sample_experiencia.nome_instituicao = nova_instituicao
    result = ExperienciaRepository.updateExperiencia(sample_experiencia, db)
    assert result.nome_instituicao == nova_instituicao



@pytest.mark.parametrize("experiencia", make_experiencias())
def test_deleteExperiencia(add_candidato, experiencia, db):
    ExperienciaRepository.createExperiencia(experiencia, db)
    result = CandidatoRepository.deleteCandidato(experiencia, db)
    assert result == True
    assert db.query(Experiencia).count() == 0

@pytest.mark.parametrize("experiencia", make_experiencias())
def test_nonExistentExperiencia_deleteExperiencia(add_candidato, experiencia, db):
    with pytest.raises(Exception):
        CandidatoRepository.deleteCandidato(experiencia, db)