import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1])) 

from ..database import Base
from ..models import Gestor, Empresa
from .repository import GestorRepository
from ..empresa.repository import EmpresaRepository


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
def test_deleteGestor(gestor, add_empresa, db):

    created_gestor = GestorRepository.createGestor(gestor, db)
    result = GestorRepository.deleteGestor(created_gestor, db)

    assert result == True
    assert db.query(Gestor).count() == 0
    
@pytest.mark.parametrize("gestor", make_gestores())
def test_deleteGestor(gestor, db):

    with pytest.raises(Exception):
        GestorRepository.deleteGestor(gestor, db)