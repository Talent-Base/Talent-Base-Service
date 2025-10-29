import os
import sys
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine, StaticPool, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
import pytest
from sqlite3 import IntegrityError

sys.path.append(str(Path(__file__).resolve().parents[2]))

try:
    dotenv_path = Path(__file__).resolve().parents[2] / ".env.testing"
    load_dotenv(dotenv_path)
except IndexError:
    print("Aviso: Caminho do arquivo .env.testing pode estar incorreto. Ignorando...")
    pass


from ..database import Base
from ..models import Gestor, Empresa
from .repository import GestorRepository
from ..empresa.repository import EmpresaRepository

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

# E não é q testes funcionam?

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def add_empresa(db):
    empresa = Empresa(
        id_empresa = 1,
        nome_empresa = "Empresa A",
        cnpj = "0000000000000",
        cidade = "Cidade A",
        estado = "AA",
        descricao = "A Empresa A é a responsavel pela saúde"
    )
    return EmpresaRepository.createEmpresa(empresa, db)


@pytest.fixture
def sample_gestor(add_empresa):

    return Gestor(
        nome = "Mariana Villasboas",
        email = "villasboas.mariana@empresaa.br",
        #id_empresa = add_empresa.id_empresa
    )


def make_gestores(valid_empresa_id: bool = True):
    if valid_empresa_id:
        id_empresa = 1
    else:
        id_empresa = -1
    
    return [
        Gestor(
            nome = "Mariana Villasboas",
            email = "villasboas.mariana@empresaa.br",
            id_empresa = id_empresa
        ),
        Gestor(
            nome = "Valquíria Saes",
            email = "saes.val@empresaa.br",
            id_empresa = id_empresa
        ),
        Gestor(
            nome = "Carlos Gomide",
            email = "gom.carlos@empresaa.br",
            id_empresa = None
        ),
    ]



@pytest.mark.parametrize("gestor", make_gestores())
def test_createGestor(gestor, add_empresa, db):

    result = GestorRepository.createGestor(gestor, db)
    
    assert result.id_gestor is not None
    assert result.nome == gestor.nome
    assert db.query(Gestor).count() == 1


@pytest.mark.parametrize("gestor", make_gestores())
def test_gestorExistsByEmail(gestor, add_empresa, db):

    GestorRepository.createGestor(gestor, db)
    result = GestorRepository.gestorExistsByEmail(gestor.email, db)
    
    assert result == True
    assert db.query(Gestor).count() == 1


@pytest.mark.parametrize("gestor", make_gestores())
def test_nonExistentGestor_gestorExistsByEmail(gestor, db):

    result = GestorRepository.gestorExistsByEmail(gestor.email, db)
    
    assert result == False
    assert db.query(Gestor).count() == 0



@pytest.mark.parametrize("gestor", make_gestores())
def test_getGestorById(gestor, add_empresa, db):

    created_gestor = GestorRepository.createGestor(gestor, db)
    result = GestorRepository.getGestorById(created_gestor.id_gestor, db)

    assert result.id_gestor == created_gestor.id_gestor
    assert result.nome == created_gestor.nome

def test_nonExistentGestor_getGestorById(db):

    result = GestorRepository.getGestorById(-1, db)

    assert result == None 

@pytest.mark.parametrize(
    "novo_email",
    ["novo1@example.com", "novo2@example.com", "novo3@example.com"]
)
def test_updateGestor(sample_gestor, novo_email, db):

    GestorRepository.createGestor(sample_gestor, db)
    sample_gestor.email = novo_email
    result = GestorRepository.updateGestor(sample_gestor, db)
    assert result.email == novo_email

@pytest.mark.parametrize("gestor", make_gestores())
def test_getGestorById(gestor, add_empresa, db):

    created_gestor = GestorRepository.createGestor(gestor, db)
    result = GestorRepository.deleteGestor(created_gestor, db)

    assert result == True
    assert db.query(Gestor).count() == 0
    
""" @pytest.mark.parametrize(
    "novo_email",
    ["novo1@example.com", "novo2@example.com", "novo3@example.com"]
)
def test_updateGestor_aaa(sample_gestor, novo_email, db):

    GestorRepository.createGestor(sample_gestor, db)
    sample_gestor.id_empresa = 999
    with pytest.raises(IntegrityError):
        GestorRepository.updateGestor(sample_gestor, db) """




""" 
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
    
    assert result.nome == "João Silva"
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
 """