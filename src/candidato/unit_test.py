import os
from sqlite3 import IntegrityError
import sys
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
import pytest

sys.path.append(str(Path(__file__).resolve().parents[2]))

try:
    dotenv_path = Path(__file__).resolve().parents[2] / ".env.testing"
    load_dotenv(dotenv_path)
except IndexError:
    print("Aviso: Caminho do arquivo .env.testing pode estar incorreto. Ignorando...")
    pass

from ..database import Base
from ..models import Candidato
from .repository import CandidatoRepository

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


# E não é q testes funcionam?

def make_candidatos():
    return [
        Candidato(
            nome="João Silva",
            email="joao@example.com",
            estado="SP",
            cidade="São Paulo",
            resumo="Experiência em FastAPI",
            situacao_empregaticia="Desempregado",
        ),
        Candidato(
            nome="Maria Souza",
            email="maria@example.com",
            estado="RJ",
            cidade="Rio de Janeiro",
            resumo="Desenvolvedora backend",
            #situacao_empregaticia="Empregado",
        ),
        Candidato(
            nome="Carlos Lima",
            email="carlos@example.com",
            #estado="MG",
            #cidade="Belo Horizonte",
            #resumo="Analista de dados",
            #situacao_empregaticia="Desempregado",
        ),
    ]

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_candidato():

    return Candidato(
        nome="João Silva",
        email="joao@example.com",
        estado="SP",
        cidade="São Paulo",
        resumo="Experiência em FastAPI",
        situacao_empregaticia="Desempregado",
    )




@pytest.mark.parametrize("candidato", make_candidatos())
def test_createCandidato(candidato, db):

    result = CandidatoRepository.createCandidato(candidato, db)
    
    assert result.id_usuario is not None
    assert result.nome == candidato.nome
    assert db.query(Candidato).count() == 1



@pytest.mark.parametrize("candidato", make_candidatos())
def test_candidatoExistsByEmail(candidato, db):

    CandidatoRepository.createCandidato(candidato, db)
    result = CandidatoRepository.candidatoExistsByEmail(candidato.email, db)
    
    assert result == True
    assert db.query(Candidato).count() == 1


@pytest.mark.parametrize("candidato", make_candidatos())
def test_nonExistentCandidato_candidatoExistsByEmail(candidato, db):

    result = CandidatoRepository.candidatoExistsByEmail(candidato.email, db)
    
    assert result == False
    assert db.query(Candidato).count() == 0




@pytest.mark.parametrize("candidato", make_candidatos())
def test_getCandidatoById(candidato, db):

    created_candidato = CandidatoRepository.createCandidato(candidato, db)
    id_created_user = created_candidato.id_usuario
    result = CandidatoRepository.getCandidatoById(id_created_user, db)

    assert result.nome == candidato.nome

def test_nonExistentCandidato_getCandidatoById( db):

    result = CandidatoRepository.getCandidatoById(1, db)

    assert result == None




@pytest.mark.parametrize(
    "novo_email",
    ["novo1@example.com", "novo2@example.com", "novo3@example.com"]
)
def test_updateCandidato(sample_candidato, novo_email, db):

    CandidatoRepository.createCandidato(sample_candidato, db)
    sample_candidato.email = novo_email
    result = CandidatoRepository.updateCandidato(sample_candidato, db)
    
    assert result.nome == sample_candidato.nome
    assert result.email == novo_email




@pytest.mark.parametrize("candidato", make_candidatos())
def test_deleteCandidato(candidato, db):

    CandidatoRepository.createCandidato(candidato, db)
    result = CandidatoRepository.deleteCandidato(candidato, db)
    
    assert result == True
    assert db.query(Candidato).count() == 0


@pytest.mark.parametrize("candidato", make_candidatos())
def test_nonExistentCandidato_deleteCandidato(candidato, db):

    with pytest.raises(Exception):
        CandidatoRepository.deleteCandidato(candidato, db)
